from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Match


MATCH_COMPLETE_AFTER = timedelta(hours=2)


def mark_finished_matches(db: Session) -> int:
    cutoff = datetime.utcnow() - MATCH_COMPLETE_AFTER
    rows = db.query(Match).filter(Match.status == "open", Match.start_time <= cutoff).all()
    for match in rows:
        match.status = "finished"
    if rows:
        db.commit()
    return len(rows)


def mark_match_finished_if_needed(db: Session, match: Match | None) -> Match | None:
    if match and match.status == "open" and match.start_time <= datetime.utcnow() - MATCH_COMPLETE_AFTER:
        match.status = "finished"
        db.commit()
        db.refresh(match)
    return match
