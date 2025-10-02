from pydantic import BaseModel
from typing import Optional, List, Literal

Level = Literal[1,2,3,4]

class PublishIn(BaseModel):
    title: str
    body: str
    link: Optional[str] = None
    levels: List[Level] = []

class ContentOut(BaseModel):
    id: int
    title: str
    body: str
    link: Optional[str] = None
    author_id: int
    published_at: str
    levels: List[Level] = []

class SendNotifIn(BaseModel):
    content_id: int
    level: Level