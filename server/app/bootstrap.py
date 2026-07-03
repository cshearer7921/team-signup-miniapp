from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import AdminUser, Team
from app.security import hash_password


def seed_initial_data(db: Session) -> None:
    settings = get_settings()
    team = db.get(Team, 1)
    if not team:
        db.add(Team(id=1, name=settings.default_team_name, description="V1 默认球队"))

    admin = db.query(AdminUser).filter_by(username=settings.admin_username).first()
    if not admin:
        db.add(
            AdminUser(
                username=settings.admin_username,
                password_hash=hash_password(settings.admin_password),
            )
        )
    db.commit()
