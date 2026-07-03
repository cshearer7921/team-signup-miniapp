# API 摘要

所有小程序 API 使用 `Authorization: Bearer <token>`。

## 登录

- `POST /api/auth/wechat-login`
- Body: `{ "code": "wx.login code", "nickname": "可选", "avatar_url": "可选" }`

## 入队申请

- `POST /api/join-requests`
- Body: `{ "name": "张三", "phone": "138...", "position": "中场", "jersey_number": "8", "message": "可选" }`

## 比赛

- `GET /api/matches`
- `GET /api/matches/{id}`
- `POST /api/matches/{id}/signup`
- Body: `{ "status": "signed_up|leave|maybe", "note": "可选" }`
- `GET /api/matches/{id}/signups`

## 个人资料

- `GET /api/me`
- `PATCH /api/me/player-profile`

## 管理员

管理员 API 使用管理员 token：

- `POST /api/auth/admin-login?username=admin&password=...`
- `GET /api/admin/dashboard`
- `GET /api/admin/join-requests`
- `POST /api/admin/join-requests/{id}/approve`
- `POST /api/admin/join-requests/{id}/reject`
- `GET /api/admin/players`
- `POST /api/admin/matches`
- `PATCH /api/admin/matches/{id}`
- `GET /api/admin/matches/{id}/export.csv`
- `GET /api/admin/matches/{id}/export.xlsx`
