import httpx
from fastapi import HTTPException

from app.config import get_settings


async def code_to_openid(code: str) -> str:
    settings = get_settings()
    if settings.wechat_mock_login:
        return f"mock_{code}"
    if not settings.wechat_appid or not settings.wechat_secret:
        raise HTTPException(status_code=500, detail="Wechat appid/secret is not configured")

    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.wechat_appid,
        "secret": settings.wechat_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient(timeout=8) as client:
        response = await client.get(url, params=params)
        data = response.json()
    if "openid" not in data:
        raise HTTPException(status_code=400, detail=f"Wechat login failed: {data}")
    return data["openid"]
