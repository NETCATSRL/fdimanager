from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
from ..schemas.users import RegisterUserIn, UserOut, ApproveUserIn
from ..db.session import get_db
from ..models.models import User, UserStatus
from ..config import TELEGRAM_BOT_TOKEN, LEVEL_CHANNELS
import httpx

router = APIRouter()


def _to_user_out(u: User) -> UserOut:
    return UserOut(
        id=u.id,
        telegram_id=u.telegram_id,
        first_name=u.first_name,
        last_name=u.last_name,
        phone=u.phone,
        email=u.email,
        level=u.level,
        status=u.status.value if isinstance(u.status, UserStatus) else u.status,
        approved_by=u.approved_by,
    )

@router.post("/register_user", response_model=UserOut)
def register_user(payload: RegisterUserIn, db: Session = Depends(get_db)):
    # upsert by telegram_id
    u = db.query(User).filter(User.telegram_id == payload.telegram_id).first()
    target_status = UserStatus.active if payload.level == 1 else UserStatus.pending
    if u:
        if u.status != UserStatus.active:
            u.status = target_status
        u.first_name = payload.first_name
        u.last_name = payload.last_name
        u.phone = payload.phone
        u.email = payload.email
        u.level = payload.level
        db.commit()
        db.refresh(u)
        return _to_user_out(u)
    u = User(
        telegram_id=payload.telegram_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
        email=payload.email,
        level=payload.level,
        status=target_status,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return _to_user_out(u)

@router.post("/approve_user")
def approve_user(payload: ApproveUserIn, db: Session = Depends(get_db)):
    u = db.get(User, payload.user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.status = UserStatus.active if payload.approve else UserStatus.rejected
    db.commit()
    return {"user_id": u.id, "status": u.status.value}

@router.get("", response_model=List[UserOut])
def list_users(level: Optional[int] = Query(None), status: Optional[str] = Query(None), db: Session = Depends(get_db)):
    q = db.query(User)
    if level is not None:
        q = q.filter(User.level == level)
    if status is not None:
        try:
            st = UserStatus(status)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid status")
        q = q.filter(User.status == st)
    users = q.order_by(User.id.asc()).all()
    return [_to_user_out(u) for u in users]

@router.post("/change_level")
async def change_level(user_id: int, level: int, db: Session = Depends(get_db)):
    if level not in (1,2,3,4):
        raise HTTPException(status_code=400, detail="Invalid level")
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    old_level = u.level
    u.level = level
    db.commit()
    # Kick from channels beyond new level if level decreased
    if TELEGRAM_BOT_TOKEN and u.telegram_id and old_level > level:
        for l in range(level + 1, old_level + 1):
            channel_id = LEVEL_CHANNELS.get(l)
            if channel_id:
                url_kick = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/banChatMember"
                payload_kick = {
                    "chat_id": channel_id,
                    "user_id": u.telegram_id,
                    "revoke_messages": False
                }
                try:
                    async with httpx.AsyncClient() as client:
                        await client.post(url_kick, json=payload_kick)
                    print(f"Kicked {u.telegram_id} from {channel_id}")
                except Exception as e:
                    print(f"Error kicking {u.telegram_id} from {channel_id}: {e}")
    # Generate invite links for all levels 1 to current level
    invite_links = []
    for l in range(1, level + 1):
        channel_id = LEVEL_CHANNELS.get(l)
        if TELEGRAM_BOT_TOKEN and channel_id:
            url_invite = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/exportChatInviteLink"
            payload_invite = {"chat_id": channel_id}
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.post(url_invite, json=payload_invite)
                    if r.status_code == 200:
                        data = r.json()
                        invite_link = data.get("result")
                        if invite_link:
                            invite_links.append(f"Livello {l}: {invite_link}")
            except Exception as e:
                print(f"Error generating invite link for level {l}: {e}")
    if TELEGRAM_BOT_TOKEN and u.telegram_id:
        text = f"Il tuo livello è stato aggiornato a {level}."
        if invite_links:
            text += "\nLink per unirti ai canali:\n" + "\n".join(invite_links)
        else:
            text += "\nContatta l'admin per accedere ai canali."
        url_send = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload_send = {"chat_id": u.telegram_id, "text": text}
        try:
            async with httpx.AsyncClient() as client:
                await client.post(url_send, json=payload_send)
        except Exception as e:
            print(f"Error sending message to {u.telegram_id}: {e}")
    return {"user_id": u.id, "level": u.level}

@router.get("/{telegram_id}", response_model=UserOut)
def get_user(telegram_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_user_out(u)

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    # Kick from all channels the user had access to
    if TELEGRAM_BOT_TOKEN and u.telegram_id:
        for l in range(1, u.level + 1):
            channel_id = LEVEL_CHANNELS.get(l)
            if channel_id:
                url_kick = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/banChatMember"
                payload_kick = {
                    "chat_id": channel_id,
                    "user_id": u.telegram_id,
                    "revoke_messages": False
                }
                try:
                    async with httpx.AsyncClient() as client:
                        await client.post(url_kick, json=payload_kick)
                    print(f"Kicked {u.telegram_id} from {channel_id} on delete")
                except Exception as e:
                    print(f"Error kicking {u.telegram_id} from {channel_id}: {e}")
    db.delete(u)
    db.commit()
    return {"deleted": True, "user_id": user_id}
