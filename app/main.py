from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api.routes import router
from .db.base import Base
from .db.session import engine, SessionLocal
from .db.models import ChampionPhrase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    # Create all tables
    print("[DATABASE] 🗄️  Initializing SQLite database...")
    Base.metadata.create_all(bind=engine)
    print("[DATABASE] ✅ Database initialized successfully!")
    
    # Seed champion phrase if not exists
    db = SessionLocal()
    try:
        champion = db.query(ChampionPhrase).filter(ChampionPhrase.id == 1).first()
        if not champion:
            champion = ChampionPhrase(id=1, phrase="Whoosa good ferret!")
            db.add(champion)
            db.commit()
            print("[DATABASE] 🏆 Seeded initial champion phrase: 'Whoosa good ferret!'")
        else:
            print(f"[DATABASE] 🏆 Champion phrase loaded: '{champion.phrase}'")
    except Exception as e:
        print(f"[DATABASE] ❌ Error seeding champion phrase: {e}")
        db.rollback()
    finally:
        db.close()
    
    yield
    # Cleanup (if needed)


app = FastAPI(
    title="Fickle Ferrets API",
    description="Share words of affirmation with our fickle ferrets and discover if you sparked joy! 🦦",
    version="0.1.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")

