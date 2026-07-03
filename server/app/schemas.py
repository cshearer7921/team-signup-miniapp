from datetime import datetime

from pydantic import BaseModel, Field


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class WechatLoginIn(BaseModel):
    code: str
    nickname: str | None = None
    avatar_url: str | None = None


class UserOut(BaseModel):
    id: int
    nickname: str | None
    avatar_url: str | None
    member_status: str | None = None
    role: str | None = None


class AuthOut(TokenOut):
    user: UserOut


class JoinRequestIn(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    phone: str | None = Field(default=None, max_length=32)
    position: str | None = Field(default=None, max_length=32)
    jersey_number: str | None = Field(default=None, max_length=16)
    message: str | None = Field(default=None, max_length=255)


class PlayerProfileIn(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    phone: str | None = Field(default=None, max_length=32)
    position: str | None = Field(default=None, max_length=32)
    jersey_number: str | None = Field(default=None, max_length=16)
    note: str | None = Field(default=None, max_length=255)


class MatchIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    opponent: str | None = Field(default=None, max_length=120)
    location: str = Field(min_length=1, max_length=255)
    start_time: datetime
    signup_deadline: datetime | None = None
    capacity: int | None = Field(default=None, ge=1)
    description: str | None = None
    status: str = "open"


class MatchOut(MatchIn):
    id: int
    signup_counts: dict[str, int] = {}
    my_signup_status: str | None = None

    class Config:
        from_attributes = True


class SignupIn(BaseModel):
    status: str = Field(pattern="^(signed_up|leave|maybe)$")
    note: str | None = Field(default=None, max_length=255)


class SignupOut(BaseModel):
    id: int
    match_id: int
    user_id: int
    status: str
    note: str | None = None

    class Config:
        from_attributes = True
