"""Service for managing A/B test experiments"""
import uuid
import random
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session

from ..db.models import Experiment, AffirmationResult, ChampionPhrase, ExperimentStatus, Variant
from ..schemas.models import ExperimentResponse
from .ferret_service import get_words_of_affirmation, process_affirmation_and_callback, create_affirmation_record


def create_experiment(
    db: Session,
    name: str,
    variant_b_phrase: str,
    target_runs: int
) -> Experiment:
    """Create a new experiment with active status
    Variant A is automatically set to the current champion phrase"""
    # Get current champion phrase - this will always be variant A
    champion = db.query(ChampionPhrase).filter(ChampionPhrase.id == 1).first()
    variant_a_phrase = champion.phrase

    # Create new experiment with active status
    experiment = Experiment(
        id=str(uuid.uuid4()),
        name=name,
        variant_a_phrase=variant_a_phrase,
        variant_b_phrase=variant_b_phrase,
        status=ExperimentStatus.ACTIVE.value,
        target_runs=target_runs,
        created_at=datetime.now()
    )

    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    print(f"[EXPERIMENT] 🧪 Created experiment '{name}' (ID: {experiment.id}, Status: active)")
    print(f"  Variant A (Champion): '{variant_a_phrase}'")
    print(f"  Variant B (Challenger): '{variant_b_phrase}'")

    return experiment

def complete_experiment(db: Session, experiment_id: str) -> None:
    """
    Complete an experiment by calculating results, determining winner,
    and updating the champion phrase
    """
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()

    if not experiment or experiment.status == ExperimentStatus.COMPLETED.value:
        return

    print(f"[EXPERIMENT] 🏁 Completing experiment '{experiment.name}' (ID: {experiment_id})")

    # Query all affirmation results for this experiment
    results = db.query(AffirmationResult).filter(
        AffirmationResult.experiment_id == experiment_id
    ).all()

    # Separate by variant (determine by matching phrase)
    variant_a_results = [r for r in results if r.words_of_affirmation == experiment.variant_a_phrase]
    variant_b_results = [r for r in results if r.words_of_affirmation == experiment.variant_b_phrase]

    # Calculate totals and wins
    variant_a_total = len(variant_a_results)
    variant_b_total = len(variant_b_results)
    variant_a_wins = sum(1 for r in variant_a_results if r.joy_sparked)
    variant_b_wins = sum(1 for r in variant_b_results if r.joy_sparked)

    # Determine winner based on win rate
    variant_a_win_rate = variant_a_wins / variant_a_total if variant_a_total > 0 else 0.0
    variant_b_win_rate = variant_b_wins / variant_b_total if variant_b_total > 0 else 0.0

    winning_variant = Variant.A if variant_a_win_rate >= variant_b_win_rate else Variant.B
    winning_phrase = experiment.variant_a_phrase if winning_variant == Variant.A else experiment.variant_b_phrase

    # Update experiment with results
    experiment.variant_a_total = variant_a_total
    experiment.variant_b_total = variant_b_total
    experiment.variant_a_wins = variant_a_wins
    experiment.variant_b_wins = variant_b_wins
    experiment.winning_variant = winning_variant.value
    experiment.status = ExperimentStatus.COMPLETED.value
    experiment.completed_at = datetime.now()

    db.commit()

    print(f"[EXPERIMENT] 📊 Results:")
    print(f"  Variant A: {variant_a_wins}/{variant_a_total} ({variant_a_win_rate:.1%})")
    print(f"  Variant B: {variant_b_wins}/{variant_b_total} ({variant_b_win_rate:.1%})")
    print(f"  Winner: Variant {winning_variant.value} - '{winning_phrase}'")

    # Update champion phrase with winner
    update_champion_phrase(db, winning_phrase)


def update_champion_phrase(db: Session, new_phrase: str) -> None:
    """Update the champion phrase in the database"""
    champion = db.query(ChampionPhrase).filter(ChampionPhrase.id == 1).first()

    if champion:
        old_phrase = champion.phrase
        champion.phrase = new_phrase
        champion.updated_at = datetime.now()
        db.commit()
        print(f"[CHAMPION] 👑 Updated champion phrase:")
        print(f"  Old: '{old_phrase}'")
        print(f"  New: '{new_phrase}'")
    else:
        print("[CHAMPION] ⚠️  No champion phrase found in database!")


async def execute_experiment(experiment_id: str, db: Session) -> None:
    """Execute all affirmations for an experiment"""
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()

    if not experiment or experiment.status != ExperimentStatus.ACTIVE.value:
        print(f"[EXPERIMENT] ⚠️  Cannot execute experiment {experiment_id} - not found or not active")
        return

    # Construct webhook URL
    webhook_url = "http://localhost:8000/webhook/ferret-reaction"

    print(f"[EXPERIMENT] 🚀 Starting {experiment.target_runs} affirmations for experiment '{experiment.name}'")

    # Create N async tasks with random 50/50 split
    tasks = []
    for _ in range(experiment.target_runs):
        phrase = get_words_of_affirmation(db)
        # Generate unique affirmation ID
        affirmation_id = str(uuid.uuid4())

        # Create database record with experiment tracking
        create_affirmation_record(
            affirmation_id=affirmation_id,
            words_of_affirmation=phrase,
            experiment_id=experiment_id
        )

        # Process affirmation with ferrets
        task = process_affirmation_and_callback(affirmation_id, phrase, webhook_url)
        tasks.append(task)

    # Execute all affirmations in parallel
    await asyncio.gather(*tasks)

    print(f"[EXPERIMENT] ✅ Completed all {experiment.target_runs} affirmations")

    # All affirmations complete, now finalize the experiment
    complete_experiment(db, experiment_id)


def build_experiment_response(experiment: Experiment) -> ExperimentResponse:
    """Build ExperimentResponse with calculated win rates"""
    # Calculate win rates on-the-fly
    variant_a_win_rate = None
    variant_b_win_rate = None

    if experiment.variant_a_total and experiment.variant_a_total > 0:
        variant_a_win_rate = experiment.variant_a_wins / experiment.variant_a_total
    if experiment.variant_b_total and experiment.variant_b_total > 0:
        variant_b_win_rate = experiment.variant_b_wins / experiment.variant_b_total

    return ExperimentResponse(
        id=experiment.id,
        name=experiment.name,
        variant_a_phrase=experiment.variant_a_phrase,
        variant_b_phrase=experiment.variant_b_phrase,
        status=experiment.status,
        target_runs=experiment.target_runs,
        created_at=experiment.created_at,
        completed_at=experiment.completed_at,
        winning_variant=experiment.winning_variant,
        variant_a_wins=experiment.variant_a_wins,
        variant_b_wins=experiment.variant_b_wins,
        variant_a_total=experiment.variant_a_total,
        variant_b_total=experiment.variant_b_total,
        variant_a_win_rate=variant_a_win_rate,
        variant_b_win_rate=variant_b_win_rate
    )
