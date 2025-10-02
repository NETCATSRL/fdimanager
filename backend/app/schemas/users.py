from pydantic import BaseModel, Field
from typing import Optional, Literal

Level = Literal[1,2,3,4]
Status = Literal['active','pending','rejected']

class RegisterUserIn(BaseModel):
    telegram_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    level: Level = 1

class UserOut(BaseModel):
    id: int
    telegram_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    level: Level
    status: Status
    approved_by: Optional[int] = None

class ApproveUserIn(BaseModel):
    user_id: int
    approve: bool = True

class ListUsersQuery(BaseModel):
    level: Optional[Level] = Field(default=None)
    status: Optional[Status] = Field(default=None)
