import asyncio
from backend.app.database.session import engine
from backend.app.models.all_models import Base

async def init_db():
    async with engine.begin() as conn:
        # In a real scenario, we would use Alembic migrations.
        # For initialization, we'll create all tables.
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
