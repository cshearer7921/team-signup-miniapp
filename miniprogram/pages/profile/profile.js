"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const request_1 = require("../../utils/request");
Page({
    data: {
        token: "",
        me: {},
        memberStatusText: "未申请",
        roleText: "-",
        miniappBuildTime: getApp().globalData.buildTime,
        serverStartedAt: "获取中"
    },
    onShow() {
        this.setData({ token: (0, request_1.getToken)() });
        if ((0, request_1.getToken)())
            this.loadMe();
        this.loadVersion();
    },
    async loadVersion() {
        try {
            const version = await (0, request_1.request)("/version");
            this.setData({ serverStartedAt: version.started_at || "未知" });
        }
        catch (error) {
            this.setData({ serverStartedAt: "获取失败" });
            console.error(error);
        }
    },
    async loadMe() {
        const me = await (0, request_1.request)("/me");
        this.setData({
            me,
            memberStatusText: statusText(me.member_status),
            roleText: roleText(me.role)
        });
    },
    goLogin() {
        wx.navigateTo({ url: "/pages/login/login" });
    },
    goJoin() {
        wx.navigateTo({ url: "/pages/join-request/join-request" });
    },
    logout() {
        wx.removeStorageSync("token");
        this.setData({ token: "", me: {}, memberStatusText: "未申请", roleText: "-" });
    }
});
function statusText(status) {
    const map = {
        pending: "待审核",
        approved: "已通过",
        rejected: "已拒绝"
    };
    return status ? map[status] || status : "未申请";
}
function roleText(role) {
    const map = {
        player: "球员",
        captain: "队长",
        admin: "管理员"
    };
    return role ? map[role] || role : "-";
}
