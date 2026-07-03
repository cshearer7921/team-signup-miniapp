from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import JoinRequest, TeamMember, User
from app.schemas import JoinRequestIn

router = APIRouter(prefix="/join-requests", tags=["join-requests"])


@router.post("")
def create_join_request(
    payload: JoinRequestIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    member = db.query(TeamMember).filter_by(team_id=1, user_id=user.id).first()
    if member and member.status == "approved":
        return {"ok": True, "status": "approved"}

    request = (
        db.query(JoinRequest)
        .filter_by(team_id=1, user_id=user.id)
        .order_by(JoinRequest.id.desc())
        .first()
    )
    if request and request.status == "pending":
        return {"ok": True, "status": "pending"}

    request = JoinRequest(team_id=1, user_id=user.id, **payload.model_dump())
    db.add(request)
    if not member:
        db.add(TeamMember(team_id=1, user_id=user.id, role="player", status="pending"))
    db.commit()
    return {"ok": True, "status": "pending"}
