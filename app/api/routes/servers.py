from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.server import Server
from schemas.server import ServerCreate, ServerResponse
from core.database import get_db

router = APIRouter()


@router.post("/", response_model=ServerResponse)
async def create_server(
        server: ServerCreate,
        db: AsyncSession = Depends(get_db)
):
    new_server = Server(**server.model_dump())
    db.add(new_server)
    await db.commit()
    await db.refresh(new_server)
    return new_server


@router.get("/", response_model=list[ServerResponse])
async def list_servers(db: AsyncSession = Depends(get_db)):
    return await db.execute(Server.__table__.select())
