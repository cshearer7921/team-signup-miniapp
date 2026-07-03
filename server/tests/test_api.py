import os
import sys
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_team_signup.db")
os.environ.setdefault("WECHAT_MOCK_LOGIN", "true")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


def test_health():
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        assert client.get("/health").json() == {"ok": True}


def test_signup_flow():
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        login = client.post("/api/auth/wechat-login", json={"code": "user_a", "nickname": "球员A"})
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        join = client.post(
            "/api/join-requests",
            json={"name": "球员A", "phone": "13800000000", "position": "中场", "jersey_number": "8"},
            headers=headers,
        )
        assert join.status_code == 200

        admin_login = client.post("/api/auth/admin-login?username=admin&password=admin123")
        assert admin_login.status_code == 200
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

        pending = client.get("/api/admin/join-requests", headers=admin_headers).json()
        request_id = next(item["id"] for item in pending if item["name"] == "球员A")
        approved = client.post(f"/api/admin/join-requests/{request_id}/approve", headers=admin_headers)
        assert approved.status_code == 200

        created = client.post(
            "/api/admin/matches",
            json={
                "title": "周末友谊赛",
                "opponent": "老友队",
                "location": "市民球场",
                "start_time": "2026-07-12T20:00:00",
                "status": "open",
            },
            headers=admin_headers,
        )
        assert created.status_code == 200
        match_id = created.json()["id"]

        signup = client.post(
            f"/api/matches/{match_id}/signup",
            json={"status": "signed_up"},
            headers=headers,
        )
        assert signup.status_code == 200
        assert signup.json()["status"] == "signed_up"
