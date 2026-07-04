from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/admin-ui", tags=["admin-ui"])


@router.get("", response_class=HTMLResponse)
def admin_ui() -> str:
    return """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>球队报名管理后台</title>
  <style>
    body{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:24px;background:#f6f7f9;color:#172033}
    main{max-width:1100px;margin:auto} section{background:#fff;border:1px solid #dde2ea;border-radius:8px;padding:16px;margin:16px 0}
    input,textarea,button{padding:9px;margin:4px;border:1px solid #cbd3df;border-radius:6px} button{background:#1769e0;color:#fff;cursor:pointer}
    table{width:100%;border-collapse:collapse} th,td{border-bottom:1px solid #edf0f5;padding:8px;text-align:left}
    .muted{color:#6b7280}
  </style>
</head>
<body>
<main>
  <h1>球队报名管理后台</h1>
  <p class="muted">V1 简单后台：登录后可审核入队、查看球员、创建比赛、导出名单。</p>
  <section>
    <h2>管理员登录</h2>
    <input id="username" placeholder="用户名" value="admin" />
    <input id="password" placeholder="密码" type="password" value="admin123" />
    <button onclick="login()">登录</button>
    <span id="loginStatus"></span>
  </section>
  <section>
    <h2>创建比赛</h2>
    <input id="title" placeholder="标题" />
    <input id="opponent" placeholder="对手" />
    <input id="location" placeholder="地点" />
    <input id="start_time" type="datetime-local" />
    <input id="capacity" type="number" placeholder="人数上限" />
    <textarea id="description" placeholder="说明"></textarea>
    <button onclick="createMatch()">创建</button>
  </section>
  <section><h2>入队申请</h2><div id="joinRequests"></div></section>
  <section><h2>球员列表</h2><div id="players"></div></section>
  <section><h2>比赛列表</h2><div id="matches"></div></section>
</main>
<script>
let token = localStorage.getItem("adminToken") || "";
const api = (path, options={}) => fetch("/api" + path, {
  ...options,
  headers: {"Content-Type":"application/json", "Authorization":"Bearer " + token, ...(options.headers || {})}
});
async function login(){
  const username = document.querySelector("#username").value;
  const password = document.querySelector("#password").value;
  const res = await fetch(`/api/auth/admin-login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {method:"POST"});
  const data = await res.json();
  if(data.access_token){ token=data.access_token; localStorage.setItem("adminToken", token); document.querySelector("#loginStatus").innerText="登录成功"; loadAll(); }
  else document.querySelector("#loginStatus").innerText=JSON.stringify(data);
}
async function loadAll(){ loadJoinRequests(); loadPlayers(); loadMatches(); }
async function loadJoinRequests(){
  const rows = await (await api("/admin/join-requests")).json();
  document.querySelector("#joinRequests").innerHTML = table(["姓名","电话","位置","号码","状态","操作"], rows.map(r => [
    r.name,r.phone||"",r.position||"",r.jersey_number||"",statusText(r.status),
    r.status==="pending" ? `<button onclick="approve(${r.id})">通过</button><button onclick="rejectReq(${r.id})">拒绝</button>` : ""
  ]));
}
async function approve(id){ await api(`/admin/join-requests/${id}/approve`, {method:"POST"}); loadAll(); }
async function rejectReq(id){ await api(`/admin/join-requests/${id}/reject`, {method:"POST"}); loadAll(); }
async function loadPlayers(){
  const rows = await (await api("/admin/players")).json();
  document.querySelector("#players").innerHTML = table(["姓名","电话","位置","号码","启用"], rows.map(r => [r.name,r.phone||"",r.position||"",r.jersey_number||"",r.is_active ? "是" : "否"]));
}
async function loadMatches(){
  const rows = await (await api("/admin/matches")).json();
  document.querySelector("#matches").innerHTML = table(["标题","对手","地点","时间","状态","导出"], rows.map(r => [
    r.title,r.opponent||"",r.location,new Date(r.start_time).toLocaleString(),matchStatusText(r.status),
    `<a href="/api/admin/matches/${r.id}/export.csv">CSV</a> <a href="/api/admin/matches/${r.id}/export.xlsx">XLSX</a>`
  ]));
}
async function createMatch(){
  const payload = {
    title: val("title"), opponent: val("opponent"), location: val("location"),
    start_time: new Date(val("start_time")).toISOString(),
    capacity: val("capacity") ? Number(val("capacity")) : null,
    description: val("description"), status: "open"
  };
  await api("/admin/matches", {method:"POST", body: JSON.stringify(payload)});
  loadMatches();
}
function val(id){ return document.querySelector("#"+id).value; }
function statusText(status){
  return ({pending:"待审核", approved:"已通过", rejected:"已拒绝"})[status] || status || "";
}
function matchStatusText(status){
  return ({open:"开放报名", closed:"已关闭", cancelled:"已取消"})[status] || status || "";
}
function table(headers, rows){
  return `<table><thead><tr>${headers.map(h=>`<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(c=>`<td>${c ?? ""}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}
if(token) loadAll();
</script>
</body>
</html>
"""
