from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_approved_member
from app.models import Match, MatchSignup, Player, TeamMember, User
from app.schemas import MatchOut, SignupIn, SignupOut
from app.services.matches import mark_finished_matches, mark_match_finished_if_needed

router = APIRouter(prefix="/matches", tags=["matches"])


def serialize_match(db: Session, match: Match, user_id: int | None = None) -> MatchOut:
    signups = db.query(MatchSignup).filter_by(match_id=match.id).all()
    counts = dict(Counter(item.status for item in signups))
    my_status = None
    if user_id:
        mine = next((item for item in signups if item.user_id == user_id), None)
        my_status = mine.status if mine else None
    data = MatchOut.model_validate(match)
    data.signup_counts = counts
    data.my_signup_status = my_status
    return data


@router.get("", response_model=list[MatchOut])
def list_matches(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[MatchOut]:
    member = db.query(TeamMember).filter_by(user_id=user.id, status="approved").first()
    if not member:
        return []
    mark_finished_matches(db)
    matches = db.query(Match).filter_by(team_id=member.team_id).order_by(Match.start_time.desc()).all()
    return [serialize_match(db, match, user.id) for match in matches]


@router.get("/{match_id}", response_model=MatchOut)
def get_match(
    match_id: int,
    user: User = Depends(require_approved_member),
    db: Session = Depends(get_db),
) -> MatchOut:
    match = db.get(Match, match_id)
    match = mark_match_finished_if_needed(db, match)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return serialize_match(db, match, user.id)


@router.post("/{match_id}/signup", response_model=SignupOut)
def signup_match(
    match_id: int,
    payload: SignupIn,
    user: User = Depends(require_approved_member),
    db: Session = Depends(get_db),
) -> MatchSignup:
    match = db.get(Match, match_id)
    match = mark_match_finished_if_needed(db, match)
    if not match or match.status != "open":
        raise HTTPException(status_code=400, detail="活动/比赛已结束，不能再报名")
    signup = db.query(MatchSignup).filter_by(match_id=match.id, user_id=user.id).first()
    if not signup:
        signup = MatchSignup(match_id=match.id, user_id=user.id, status=payload.status)
        db.add(signup)
    signup.status = payload.status
    signup.note = payload.note
    db.commit()
    db.refresh(signup)
    return signup


@router.get("/{match_id}/signups")
def match_signups(
    match_id: int,
    user: User = Depends(require_approved_member),
    db: Session = Depends(get_db),
) -> list[dict]:
    mark_match_finished_if_needed(db, db.get(Match, match_id))
    rows = db.query(MatchSignup).filter_by(match_id=match_id).all()
    result = []
    for row in rows:
        player = db.query(Player).filter_by(user_id=row.user_id).first()
        result.append(
            {
                "user_id": row.user_id,
                "player_name": player.name if player else f"用户{row.user_id}",
                "position": player.position if player else None,
                "jersey_number": player.jersey_number if player else None,
                "status": row.status,
                "note": row.note,
                "updated_at": row.updated_at,
            }
        )
    return result
