from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AdminUser, TeamMember, User
from app.schemas import AuthOut, TokenOut, UserOut, WechatLoginIn
from app.security import create_token, verify_password
from app.services.wechat import code_to_openid

router = APIRouter(prefix="/auth", tags=["auth"])


def build_user_out(db: Session, user: User) -> UserOut:
    member = db.query(TeamMember).filter_by(user_id=user.id).first()
    return UserOut(
        id=user.id,
        nickname=user.nickname,
        avatar_url=user.avatar_url,
        member_status=member.status if member else None,
        role=member.role if member else None,
    )


@router.post("/wechat-login", response_model=AuthOut)
async def wechat_login(payload: WechatLoginIn, db: Session = Depends(get_db)) -> AuthOut:
    openid = await code_to_openid(payload.code)
    user = db.query(User).filter_by(openid=openid).first()
    if not user:
        user = User(openid=openid, nickname=payload.nickname, avatar_url=payload.avatar_url)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.nickname = payload.nickname or user.nickname
        user.avatar_url = payload.avatar_url or user.avatar_url
        db.commit()

    return AuthOut(access_token=create_token(str(user.id), "user"), user=build_user_out(db, user))


@router.post("/admin-login", response_model=TokenOut)
def admin_login(username: str, password: str, db: Session = Depends(get_db)) -> TokenOut:
    admin = db.query(AdminUser).filter_by(username=username).first()
    if not admin or not admin.is_active or not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    return TokenOut(access_token=create_token(str(admin.id), "admin"))
