"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const request_1 = require("../../utils/request");
const statusMap = { signed_up: "报名", leave: "请假", maybe: "待定" };
const matchStatusMap = {
    open: "开放报名",
    finished: "已完成",
    closed: "已关闭",
    cancelled: "已取消"
};
Page({
    data: {
        id: 0,
        match: {},
        signups: [],
        displayMembers: [],
        signupStats: { signed_up: 0, leave: 0, maybe: 0, total: 0 },
        displayTime: "",
        organizerInitial: "云",
        organizerName: "云桥FC",
        matchStatusText: "",
        statusText: "未报名"
    },
    onLoad(query) {
        this.setData({ id: Number(query.id) });
        this.load();
    },
    async load() {
        const match = await (0, request_1.request)(`/matches/${this.data.id}`);
        const signups = await (0, request_1.request)(`/matches/${this.data.id}/signups`);
        const signupStats = buildStats(signups);
        this.setData({
            match,
            signups,
            signupStats,
            displayMembers: buildMembers(signups),
            displayTime: formatDateTime(match.start_time),
            matchStatusText: matchStatusMap[match.status] || match.status || "-",
            statusText: statusMap[match.my_signup_status] || "未报名"
        });
    },
    async signup(event) {
        const status = event.currentTarget.dataset.status;
        await (0, request_1.request)(`/matches/${this.data.id}/signup`, "POST", { status });
        wx.showToast({ title: "已提交", icon: "success" });
        this.load();
    }
});
function buildStats(rows) {
    const stats = { signed_up: 0, leave: 0, maybe: 0, total: rows.length };
    rows.forEach((row) => {
        stats[row.status] += 1;
    });
    return stats;
}
function buildMembers(rows) {
    if (!rows.length) {
        return [
            { key: "empty-1", name: "等待报名", initial: "+", status: "empty", statusText: "" },
            { key: "empty-2", name: "邀请队友", initial: "+", status: "empty", statusText: "" }
        ];
    }
    return rows.map((row) => ({
        key: row.user_id,
        name: row.player_name,
        initial: row.player_name ? row.player_name.slice(0, 1) : "队",
        status: row.status,
        statusText: statusMap[row.status]
    }));
}
function formatDateTime(value) {
    if (!value)
        return "活动时间待定";
    const date = new Date(value);
    if (Number.isNaN(date.getTime()))
        return value;
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const weekday = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][date.getDay()];
    const hour = String(date.getHours()).padStart(2, "0");
    const minute = String(date.getMinutes()).padStart(2, "0");
    return `${month}月${day}日-${weekday} ${hour}:${minute}`;
}
