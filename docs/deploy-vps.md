# VPS 部署说明

## 1. 准备服务器

- 安装 Docker 和 Docker Compose。
- 将域名解析到 VPS 公网 IP。
- 在微信小程序后台把 `https://你的域名` 配置为合法请求域名。

## 2. 配置环境变量

```bash
cp .env.example .env
vim .env
```

至少修改：

- `DOMAIN`
- `MYSQL_PASSWORD`
- `MYSQL_ROOT_PASSWORD`
- `DATABASE_URL` 中的密码
- `JWT_SECRET`
- `WECHAT_APPID`
- `WECHAT_SECRET`
- `ADMIN_PASSWORD`

## 3. 配置 HTTPS 证书

把证书放到：

```text
deploy/certs/fullchain.pem
deploy/certs/privkey.pem
```

如果使用 Let's Encrypt，可以先临时注释 Nginx 的 443 server，申请证书后再恢复。

## 4. 启动

```bash
docker compose up -d --build
docker compose ps
curl https://你的域名/health
```

后台地址：

```text
https://你的域名/admin-ui
```

## 5. 数据备份

```bash
bash deploy/scripts/backup_mysql.sh
```

恢复：

```bash
bash deploy/scripts/restore_mysql.sh backups/team_signup_YYYYMMDD_HHMMSS.sql.gz
```
