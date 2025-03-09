from fastapi import APIRouter, Depends
from fastapi.responses import Response
from prometheus_client import generate_latest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.server import Server
from core.database import get_db
from services.monitoring import check_server
import asyncio

router = APIRouter()


@router.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")


@router.get("/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Server).where(Server.is_active == True))
    servers = result.scalars().all()

    tasks = [check_server(server.url) for server in servers]
    return await asyncio.gather(*tasks)
