"""Service for processing ferret affirmations and interactions"""
import httpx
import asyncio
import random
import traceback
from datetime import datetime
from sqlalchemy.orm import Session

from ..db.models import AffirmationResult, ChampionPhrase, Experiment, ExperimentStatus, Variant
from ..db.session import SessionLocal


def get_words_of_affirmation(db: Session) -> str:
    """Get words of affirmation - either from champion or from a running experiment.

    Returns:
        str: Words of affirmation
            - If no experiment is running: returns champion phrase
            - If experiment is running: returns randomly selected variant (50/50 chance)
    """
    # Check if there's an active experiment
    active_experiment = db.query(Experiment).filter(
        Experiment.status == ExperimentStatus.ACTIVE.value
    ).first()

    if active_experiment:
        # 50/50 chance between variant A and variant B
        selected_variant = random.choice([Variant.A, Variant.B])

        if selected_variant == Variant.A:
            return active_experiment.variant_a_phrase
        else:
            return active_experiment.variant_b_phrase
    else:
        # No active experiment, use the champion phrase
        champion = db.query(ChampionPhrase).filter(ChampionPhrase.id == 1).first()

        return champion.phrase


def create_affirmation_record(
    affirmation_id: str,
    words_of_affirmation: str,
    experiment_id: str | None = None
) -> None:
    """Create initial database record for new affirmation"""
    db = SessionLocal()
    try:
        # Create a temporary record with joy_sparked=False (will be updated later)
        db_affirmation = AffirmationResult(
            affirmation_id=affirmation_id,
            words_of_affirmation=words_of_affirmation,
            joy_sparked=False,  # Placeholder, will be updated
            created_at=datetime.now(),
            experiment_id=experiment_id
        )
        db.add(db_affirmation)
        db.commit()
        print(f"[DATABASE] 💾 Created affirmation record: {affirmation_id}")
    except Exception as e:
        print(f"[DATABASE] ❌ Error creating affirmation record: {e}")
        db.rollback()
    finally:
        db.close()


def update_affirmation_result(affirmation_id: str, joy_sparked: bool) -> None:
    """Update affirmation record with ferret reaction result"""
    db = SessionLocal()
    try:
        db_affirmation = db.query(AffirmationResult).filter(
            AffirmationResult.affirmation_id == affirmation_id
        ).first()
        
        if db_affirmation:
            db_affirmation.joy_sparked = joy_sparked
            db_affirmation.callback_received_at = datetime.now()
            db.commit()
            print(f"[DATABASE] 💾 Updated affirmation result: {affirmation_id} (joy={joy_sparked})")
        else:
            print(f"[DATABASE] ⚠️  Affirmation not found: {affirmation_id}")
    except Exception as e:
        print(f"[DATABASE] ❌ Error updating affirmation result: {e}")
        db.rollback()
    finally:
        db.close()


async def process_affirmation_and_callback(affirmation_id: str, words_of_affirmation: str, webhook_url: str) -> None:
    """Background task that shares words with ferrets, waits for their reaction, then posts to webhook"""
    try:
        # Share words with the fickle ferrets
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"[FERRETS] 🦦 Sharing affirmation {affirmation_id} with our fickle ferrets...")
            response = await client.post(
                "https://spark-joy.local-services.workers.dev/spark",
                json={"input": words_of_affirmation},
                headers={"Content-Type": "application/json"}
            )
            ferret_joy = response.json()["result"]
            
            # Ferrets are thinking... (they're very fickle and take their time)
            delay = random.uniform(0.0, 1.0)
            print(f"[FERRETS] 🤔 Ferrets are contemplating... ({delay:.2f} seconds)")
            await asyncio.sleep(delay)
            
            # Post ferret reaction to our webhook endpoint
            callback_payload = {
                "affirmation_id": affirmation_id,
                "joy_sparked": ferret_joy,
                "timestamp": datetime.now().isoformat()
            }
            print(f"[FERRETS] 📢 Posting ferret reaction to webhook...")
            await client.post(webhook_url, json=callback_payload)
            print(f"[FERRETS] {'✨ Ferrets sparked with joy!' if ferret_joy else '😔 Ferrets remain unimpressed.'} (ID: {affirmation_id})")
    except Exception as e:
        print(f"[FERRETS] ❌ Error processing affirmation {affirmation_id}: {type(e).__name__}: {e}")
        print(f"[FERRETS] 📋 Traceback: {traceback.format_exc()}")

