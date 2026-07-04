"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const request_1 = require("../../utils/request");
Page({
    data: {
        token: "",
        matches: []
    },
    onShow() {
        this.setData({ token: (0, request_1.getToken)() });
        if ((0, request_1.getToken)())
            this.loadMatches();
    },
    async loadMatches() {
        try {
            const rows = await (0, request_1.request)("/matches");
            const matches = rows.map((item) => ({
                ...item,
                status_text: matchStatusText(item.status)
            }));
            this.setData({ matches });
        }
        catch (error) {
            console.error(error);
        }
    },
    goLogin() {
        wx.navigateTo({ url: "/pages/login/login" });
    },
    goJoin() {
        wx.navigateTo({ url: "/pages/join-request/join-request" });
    },
    goCreate() {
        wx.switchTab({ url: "/pages/create-activity/create-activity" });
    },
    openMatch(event) {
        wx.navigateTo({ url: `/pages/match-detail/match-detail?id=${event.currentTarget.dataset.id}` });
    }
});
function matchStatusText(status) {
    const map = {
        open: "开放报名",
        finished: "已完成",
        closed: "已关闭",
        cancelled: "已取消"
    };
    return status ? map[status] || status : "-";
}
