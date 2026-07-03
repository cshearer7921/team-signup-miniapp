"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const request_1 = require("../../utils/request");
const statusMap = { signed_up: "报名", leave: "请假", maybe: "待定" };
Page({
    data: {
        id: 0,
        match: {},
        signups: [],
        statusMap,
        statusText: "未报名"
    },
    onLoad(query) {
        this.setData({ id: Number(query.id) });
        this.load();
    },
    async load() {
        const match = await (0, request_1.request)(`/matches/${this.data.id}`);
        const signups = await (0, request_1.request)(`/matches/${this.data.id}/signups`);
        this.setData({
            match,
            signups,
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
