"""API route handlers"""
from fastapi import APIRouter, status, BackgroundTasks, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session

from app.schemas.models import (
    Message,
    AffirmationResponse,
    WebhookCallback,
    AffirmationHistoryItem,
    ChampionPhraseResponse,
    ExperimentCreate,
    ExperimentResponse
)
from app.services.ferret_service import (
    get_words_of_affirmation,
    update_affirmation_result,
    create_affirmation_record,
    process_affirmation_and_callback
)
from app.services.experiment_service import (
    create_experiment,
    execute_experiment,
    build_experiment_response
)
from app.db.session import get_db
from app.db.models import AffirmationResult, ChampionPhrase, Experiment, ExperimentStatus

router = APIRouter()


@router.get("/", response_model=Message)
async def root() -> Message:
    """Root endpoint returning a welcome message"""
    return Message(message="Welcome to Fickle Ferrets! 🦦 Share your words of affirmation and see if you can spark joy in our discerning ferrets. Visit /docs for interactive documentation.")


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@router.post("/webhook/ferret-reaction")
async def webhook_ferret_reaction(callback: WebhookCallback, db: Session = Depends(get_db)) -> dict[str, str]:
    """Webhook endpoint to receive ferret joy reactions"""
    print(f"[WEBHOOK] 📬 Received ferret reaction for affirmation {callback.affirmation_id}")
    print(f"[WEBHOOK] 🦦 Ferret Response: {'✨ JOY SPARKED!' if callback.joy_sparked else '😑 Unimpressed.'}")
    print(f"[WEBHOOK] ⏰ Timestamp: {callback.timestamp}")
    
    # Update database with ferret reaction
    update_affirmation_result(callback.affirmation_id, callback.joy_sparked, db=db)
    
    return {"status": "received", "affirmation_id": callback.affirmation_id}


@router.post("/affirmation", response_model=AffirmationResponse, status_code=status.HTTP_202_ACCEPTED)
async def share_affirmation(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> AffirmationResponse:
    """Share the champion affirmation with our fickle ferrets - returns immediately and processes asynchronously"""
    words_of_affirmation = get_words_of_affirmation(db)

    # Generate unique affirmation ID
    affirmation_id = str(uuid.uuid4())
    
    # Create database record for this affirmation
    create_affirmation_record(affirmation_id, words_of_affirmation, db)
    
    # Construct webhook URL (assuming localhost for development)
    webhook_url = "http://localhost:8000/webhook/ferret-reaction"
    
    # Add background task to share affirmation with ferrets and get their reaction
    background_tasks.add_task(
        process_affirmation_and_callback,
        affirmation_id,
        words_of_affirmation,
        webhook_url
    )
    
    print(f"[AFFIRMATION] 🦦 New affirmation received! ID: {affirmation_id}")
    print(f"[AFFIRMATION] 📝 Using champion phrase: '{words_of_affirmation}'")

    # Return immediately with affirmation ID
    return AffirmationResponse(
        affirmation_id=affirmation_id,
        message="Your words have been shared with the ferrets! They're contemplating... 🦦"
    )


@router.get("/champion", response_model=ChampionPhraseResponse)
async def get_champion_phrase(db: Session = Depends(get_db)) -> ChampionPhraseResponse:
    """Get the current champion phrase"""
    champion = db.query(ChampionPhrase).filter(ChampionPhrase.id == 1).first()
    return ChampionPhraseResponse(
        phrase=champion.phrase,
        updated_at=champion.updated_at
    )


@router.get("/affirmations/history", response_model=list[AffirmationHistoryItem])
async def get_affirmation_history(
    limit: int = 50,
    db: Session = Depends(get_db)
) -> list[AffirmationHistoryItem]:
    """Get history of affirmations and ferret reactions"""
    # Query database for recent affirmations
    results = db.query(AffirmationResult).order_by(
        AffirmationResult.created_at.desc()
    ).limit(limit).all()

    # Convert to response models
    return [
        AffirmationHistoryItem(
            affirmation_id=result.affirmation_id,
            words_of_affirmation=result.words_of_affirmation,
            joy_sparked=result.joy_sparked,
            created_at=result.created_at,
            callback_received_at=result.callback_received_at
        )
        for result in results
    ]


@router.post("/experiments", response_model=ExperimentResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_new_experiment(
    experiment: ExperimentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> ExperimentResponse:
    """Create a new A/B test experiment - auto-activates and runs if no other experiment is active
    Variant A is automatically set to the current champion phrase"""
    # Check if there's already an active experiment
    active_experiment = db.query(Experiment).filter(Experiment.status == ExperimentStatus.ACTIVE.value).first()

    if active_experiment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An experiment is already active: '{active_experiment.name}' (ID: {active_experiment.id}). Please wait for it to complete before creating a new one."
        )

    new_experiment = create_experiment(
        db=db,
        name=experiment.name,
        variant_b_phrase=experiment.variant_b_phrase,
        target_runs=experiment.target_runs
    )
    # Automatically execute the experiment in the background
    background_tasks.add_task(execute_experiment, new_experiment.id, db)
    print(f"[EXPERIMENT] 🎬 Queued automatic execution for experiment '{new_experiment.name}'")

    return build_experiment_response(new_experiment)


@router.get("/experiments", response_model=list[ExperimentResponse])
async def list_experiments(
    status_filter: str | None = None,
    db: Session = Depends(get_db)
) -> list[ExperimentResponse]:
    """List all experiments, optionally filtered by status (active, completed)"""
    query = db.query(Experiment)

    if status_filter:
        query = query.filter(Experiment.status == status_filter)

    experiments = query.order_by(Experiment.created_at.desc()).all()

    return [build_experiment_response(exp) for exp in experiments]


@router.get("/experiments/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(
    experiment_id: str,
    db: Session = Depends(get_db)
) -> ExperimentResponse:
    """Get details for a specific experiment, including results if completed"""
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()

    if not experiment:
        raise HTTPException(status_code=404, detail=f"Experiment {experiment_id} not found")

    return build_experiment_response(experiment)



