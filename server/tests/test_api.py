import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_team_signup.db")
os.environ.setdefault("WECHAT_MOCK_LOGIN", "true")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app
from app.services.matches import as_app_time, current_app_time


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


def test_match_auto_finished_after_two_hours():
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        login = client.post("/api/auth/wechat-login", json={"code": "user_b", "nickname": "球员B"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        client.post(
            "/api/join-requests",
            json={"name": "球员B", "phone": "13900000000", "position": "后卫", "jersey_number": "5"},
            headers=headers,
        )

        admin_login = client.post("/api/auth/admin-login?username=admin&password=admin123")
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
        pending = client.get("/api/admin/join-requests", headers=admin_headers).json()
        request_id = next(item["id"] for item in pending if item["name"] == "球员B")
        client.post(f"/api/admin/join-requests/{request_id}/approve", headers=admin_headers)

        old_start_time = (current_app_time() - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S")
        created = client.post(
            "/api/admin/matches",
            json={
                "title": "已结束测试赛",
                "opponent": "测试队",
                "location": "测试球场",
                "start_time": old_start_time,
                "status": "open",
            },
            headers=admin_headers,
        )
        match_id = created.json()["id"]

        matches = client.get("/api/matches", headers=headers).json()
        target = next(item for item in matches if item["id"] == match_id)
        assert target["status"] == "finished"

        signup = client.post(
            f"/api/matches/{match_id}/signup",
            json={"status": "signed_up"},
            headers=headers,
        )
        assert signup.status_code == 400


def test_timezone_aware_match_time_is_normalized_to_beijing_time():
    utc_time = datetime.fromisoformat("2026-07-04T06:00:00+00:00")
    assert as_app_time(utc_time) == datetime(2026, 7, 4, 14, 0, 0)


def test_approved_member_can_create_match_from_miniapp():
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        login = client.post("/api/auth/wechat-login", json={"code": "user_c", "nickname": "球员C"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        client.post(
            "/api/join-requests",
            json={"name": "球员C", "phone": "13700000000", "position": "前锋", "jersey_number": "9"},
            headers=headers,
        )
        admin_login = client.post("/api/auth/admin-login?username=admin&password=admin123")
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
        pending = client.get("/api/admin/join-requests", headers=admin_headers).json()
        request_id = next(item["id"] for item in pending if item["name"] == "球员C")
        client.post(f"/api/admin/join-requests/{request_id}/approve", headers=admin_headers)

        created = client.post(
            "/api/matches",
            json={
                "title": "手机端发起活动",
                "opponent": "社区队",
                "location": "云桥球场",
                "start_time": "2026-08-01T19:30:00",
                "capacity": 18,
                "description": "手机端创建",
                "status": "open",
            },
            headers=headers,
        )
        assert created.status_code == 200
        assert created.json()["title"] == "手机端发起活动"
        assert created.json()["status"] == "open"
