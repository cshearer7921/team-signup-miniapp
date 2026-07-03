"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const request_1 = require("../../utils/request");
Page({
    data: {
        token: "",
        me: {}
    },
    onShow() {
        this.setData({ token: (0, request_1.getToken)() });
        if ((0, request_1.getToken)())
            this.loadMe();
    },
    async loadMe() {
        const me = await (0, request_1.request)("/me");
        this.setData({ me });
    },
    goLogin() {
        wx.navigateTo({ url: "/pages/login/login" });
    },
    goJoin() {
        wx.navigateTo({ url: "/pages/join-request/join-request" });
    },
    logout() {
        wx.removeStorageSync("token");
        this.setData({ token: "", me: {} });
    }
});
