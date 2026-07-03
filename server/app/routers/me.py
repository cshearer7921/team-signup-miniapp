from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Player, TeamMember, User
from app.routers.auth import build_user_out
from app.schemas import PlayerProfileIn, UserOut

router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=UserOut)
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> UserOut:
    return build_user_out(db, user)


@router.patch("/player-profile")
def update_profile(
    payload: PlayerProfileIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    member = db.query(TeamMember).filter_by(user_id=user.id, status="approved").first()
    if not member:
        raise HTTPException(status_code=403, detail="Team membership is not approved")
    player = db.query(Player).filter_by(user_id=user.id, team_id=member.team_id).first()
    if not player:
        player = Player(user_id=user.id, team_id=member.team_id, name=payload.name)
        db.add(player)
    player.name = payload.name
    player.phone = payload.phone
    player.position = payload.position
    player.jersey_number = payload.jersey_number
    player.note = payload.note
    db.commit()
    return {"ok": True}
