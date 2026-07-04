from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models import Match


MATCH_COMPLETE_AFTER = timedelta(hours=2)
APP_TIMEZONE = ZoneInfo("Asia/Shanghai")


def current_app_time() -> datetime:
    return datetime.now(APP_TIMEZONE).replace(tzinfo=None)


def as_app_time(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value
    return value.astimezone(APP_TIMEZONE).replace(tzinfo=None)


def finish_cutoff() -> datetime:
    return current_app_time() - MATCH_COMPLETE_AFTER


def mark_finished_matches(db: Session) -> int:
    cutoff = finish_cutoff()
    rows = db.query(Match).filter(Match.status == "open", Match.start_time <= cutoff).all()
    for match in rows:
        match.status = "finished"
    if rows:
        db.commit()
    return len(rows)


def mark_match_finished_if_needed(db: Session, match: Match | None) -> Match | None:
    if match and match.status == "open" and match.start_time <= finish_cutoff():
        match.status = "finished"
        db.commit()
        db.refresh(match)
    return match
