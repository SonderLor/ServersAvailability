from fastapi import FastAPI
from api.routes import servers, metrics

app = FastAPI()

app.include_router(servers.router, prefix="/servers", tags=["servers"])
app.include_router(metrics.router, prefix="/monitoring", tags=["monitoring"])
