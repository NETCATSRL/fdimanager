
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..schemas.contents import PublishIn, ContentOut, SendNotifIn
from ..db.session import get_db
from ..models.models import Content, ContentVisibility, User
import os

router = APIRouter()

LEVEL_CHANNELS = {
    1: os.getenv("TELEGRAM_LEVEL1_CHANNEL_ID"),
    2: os.getenv("TELEGRAM_LEVEL2_CHANNEL_ID"),
    3: os.getenv("TELEGRAM_LEVEL3_CHANNEL_ID"),
    4: os.getenv("TELEGRAM_LEVEL4_CHANNEL_ID"),
}

def _to_content_out(c: Content, db: Session) -> ContentOut:
    levels = db.execute(select(ContentVisibility.level_target).where(ContentVisibility.content_id == c.id, ContentVisibility.level_target.isnot(None))).scalars().all()
    return ContentOut(
        id=c.id,
        title=c.title,
        body=c.body,
        link=c.link,
        author_id=c.author_id,
        published_at=c.published_at.isoformat() if c.published_at else datetime.utcnow().isoformat(),
        levels=list(set(levels))
    )

@router.post("/publish_content")
def publish_content(payload: PublishIn, db: Session = Depends(get_db)):
    # author_id=0 for MVP (no auth yet)
    content = Content(title=payload.title, body=payload.body, link=payload.link, author_id=0)
    db.add(content)
    db.flush()

    # store visibility
    for lvl in (payload.levels or []):
        db.add(ContentVisibility(content_id=content.id, level_target=lvl))

    db.commit()

    return {"content_id": content.id, "levels": payload.levels}

@router.post("/send_notification")
def send_notification(payload: SendNotifIn, db: Session = Depends(get_db)):
    c = db.get(Content, payload.content_id)
    if not c:
        raise HTTPException(status_code=404, detail="Content not found")

    channel_id = LEVEL_CHANNELS.get(payload.level)
    if not channel_id:
        raise HTTPException(status_code=400, detail=f"Channel for level {payload.level} not configured")

    # Here you would implement the logic to send a message to the Telegram channel
    # For now, we just simulate it by printing to the console
    print(f"Simulating sending notification for content {c.id} to channel {channel_id} for level {payload.level}")
    
    return {"content_id": c.id, "level": payload.level, "channel_id": channel_id, "status": "sent"}

@router.get("/history", response_model=List[ContentOut])
def get_history(db: Session = Depends(get_db)):
    items = db.execute(select(Content)).scalars().all()
    items.sort(key=lambda c: c.published_at, reverse=True)
    return [_to_content_out(c, db) for c in items]
