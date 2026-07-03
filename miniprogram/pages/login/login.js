"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const request_1 = require("../../utils/request");
Page({
    async login() {
        try {
            const wxLogin = await wx.login();
            const res = await (0, request_1.request)("/auth/wechat-login", "POST", {
                code: wxLogin.code,
                nickname: "微信用户"
            });
            (0, request_1.setToken)(res.access_token);
            wx.switchTab({ url: "/pages/index/index" });
        }
        catch (error) {
            wx.showToast({ title: "登录失败", icon: "error" });
            console.error(error);
        }
    }
});
