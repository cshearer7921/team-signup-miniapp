from io import BytesIO, StringIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_admin
from app.models import AdminUser, AuditLog, JoinRequest, Match, MatchSignup, Player, TeamMember
from app.schemas import MatchIn, MatchOut

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(get_current_admin)])


def audit(db: Session, admin: AdminUser, action: str, target_type: str, target_id: int | None) -> None:
    db.add(AuditLog(actor_type="admin", actor_id=admin.id, action=action, target_type=target_type, target_id=target_id))


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)) -> dict:
    return {
        "players": db.query(Player).count(),
        "pending_join_requests": db.query(JoinRequest).filter_by(status="pending").count(),
        "matches": db.query(Match).count(),
    }


@router.get("/join-requests")
def list_join_requests(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.query(JoinRequest).order_by(JoinRequest.id.desc()).all()
    return [
        {
            "id": row.id,
            "name": row.name,
            "phone": row.phone,
            "position": row.position,
            "jersey_number": row.jersey_number,
            "message": row.message,
            "status": row.status,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@router.post("/join-requests/{request_id}/approve")
def approve_join_request(
    request_id: int,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> dict:
    request = db.get(JoinRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Join request not found")
    request.status = "approved"
    member = db.query(TeamMember).filter_by(team_id=request.team_id, user_id=request.user_id).first()
    if not member:
        member = TeamMember(team_id=request.team_id, user_id=request.user_id, role="player")
        db.add(member)
    member.status = "approved"
    player = db.query(Player).filter_by(user_id=request.user_id, team_id=request.team_id).first()
    if not player:
        db.add(
            Player(
                user_id=request.user_id,
                team_id=request.team_id,
                name=request.name,
                phone=request.phone,
                position=request.position,
                jersey_number=request.jersey_number,
            )
        )
    audit(db, admin, "approve_join_request", "join_request", request.id)
    db.commit()
    return {"ok": True}


@router.post("/join-requests/{request_id}/reject")
def reject_join_request(
    request_id: int,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> dict:
    request = db.get(JoinRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Join request not found")
    request.status = "rejected"
    member = db.query(TeamMember).filter_by(team_id=request.team_id, user_id=request.user_id).first()
    if member:
        member.status = "rejected"
    audit(db, admin, "reject_join_request", "join_request", request.id)
    db.commit()
    return {"ok": True}


@router.get("/players")
def list_players(db: Session = Depends(get_db)) -> list[dict]:
    return [
        {
            "id": row.id,
            "name": row.name,
            "phone": row.phone,
            "position": row.position,
            "jersey_number": row.jersey_number,
            "is_active": row.is_active,
        }
        for row in db.query(Player).order_by(Player.name.asc()).all()
    ]


@router.post("/matches", response_model=MatchOut)
def create_match(
    payload: MatchIn,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Match:
    match = Match(team_id=1, **payload.model_dump())
    db.add(match)
    db.flush()
    audit(db, admin, "create_match", "match", match.id)
    db.commit()
    db.refresh(match)
    return match


@router.patch("/matches/{match_id}", response_model=MatchOut)
def update_match(
    match_id: int,
    payload: MatchIn,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Match:
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    for key, value in payload.model_dump().items():
        setattr(match, key, value)
    audit(db, admin, "update_match", "match", match.id)
    db.commit()
    db.refresh(match)
    return match


@router.get("/matches")
def admin_matches(db: Session = Depends(get_db)) -> list[dict]:
    return [
        {"id": row.id, "title": row.title, "opponent": row.opponent, "location": row.location, "start_time": row.start_time, "status": row.status}
        for row in db.query(Match).order_by(Match.start_time.desc()).all()
    ]


def signup_export_rows(db: Session, match_id: int) -> list[list[str]]:
    rows = [["姓名", "位置", "号码", "状态", "备注", "更新时间"]]
    signups = db.query(MatchSignup).filter_by(match_id=match_id).all()
    for signup in signups:
        player = db.query(Player).filter_by(user_id=signup.user_id).first()
        rows.append(
            [
                player.name if player else f"用户{signup.user_id}",
                player.position or "" if player else "",
                player.jersey_number or "" if player else "",
                signup.status,
                signup.note or "",
                signup.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )
    return rows


@router.get("/matches/{match_id}/export.csv")
def export_signups_csv(match_id: int, db: Session = Depends(get_db)) -> Response:
    rows = signup_export_rows(db, match_id)
    output = StringIO()
    for row in rows:
        output.write(",".join(f'"{str(cell).replace(chr(34), chr(34) + chr(34))}"' for cell in row) + "\n")
    return Response(
        content="\ufeff" + output.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="match_{match_id}_signups.csv"'},
    )


@router.get("/matches/{match_id}/export.xlsx")
def export_signups_xlsx(match_id: int, db: Session = Depends(get_db)) -> Response:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "报名名单"
    for row in signup_export_rows(db, match_id):
        sheet.append(row)
    stream = BytesIO()
    workbook.save(stream)
    return Response(
        content=stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="match_{match_id}_signups.xlsx"'},
    )
