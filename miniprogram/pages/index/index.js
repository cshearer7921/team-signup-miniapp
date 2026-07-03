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
            const matches = await (0, request_1.request)("/matches");
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
    openMatch(event) {
        wx.navigateTo({ url: `/pages/match-detail/match-detail?id=${event.currentTarget.dataset.id}` });
    }
});
