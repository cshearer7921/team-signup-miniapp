# 业余球队比赛报名系统 V1

微信原生小程序 + FastAPI + MySQL + Redis + Docker Compose + Nginx + HTTPS。

V1 目标：队长发布比赛，球员微信登录后申请入队，审核通过后可报名、请假或待定，队长可在简单 Web 后台管理比赛和导出名单。

## 项目结构

```text
team-signup-miniapp/
  miniprogram/       微信原生小程序 TypeScript
  server/            FastAPI 后端
  deploy/            Nginx、备份脚本
  docs/              API 和 VPS 部署说明
  docker-compose.yml
  .env.example
```

## 本地启动后端

```powershell
cd F:\CodexAIwork\team-signup-miniapp\server
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:DATABASE_URL="sqlite:///./local.db"
$env:WECHAT_MOCK_LOGIN="true"
uvicorn app.main:app --reload
```

访问：

- API 文档：http://127.0.0.1:8000/docs
- 管理后台：http://127.0.0.1:8000/admin-ui
- 健康检查：http://127.0.0.1:8000/health

默认后台账号来自环境变量：

- 用户名：`admin`
- 密码：`admin123`

生产环境必须修改 `.env` 中的 `ADMIN_PASSWORD` 和 `JWT_SECRET`。

## 小程序开发

1. 使用微信开发者工具打开 `miniprogram/`。
2. 复制 `project.private.config.json.example` 为 `project.private.config.json`，填写小程序 AppID。
3. 修改 `miniprogram/app.ts` 中的 `apiBaseUrl` 为你的 HTTPS API 地址，例如：

```ts
apiBaseUrl: "https://example.com/api"
```

## VPS 部署

见 [docs/deploy-vps.md](docs/deploy-vps.md)。

核心命令：

```bash
cp .env.example .env
docker compose up -d --build
```

## GitHub 提交

```bash
git init
git add .
git commit -m "Initial team signup miniapp V1"
git branch -M main
git remote add origin git@github.com:<你的用户名>/team-signup-miniapp.git
git push -u origin main
```
