from pydantic import BaseModel


class ServerCreate(BaseModel):
    name: str
    url: str


class ServerResponse(ServerCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
