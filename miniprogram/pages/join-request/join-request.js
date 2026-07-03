"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const request_1 = require("../../utils/request");
Page({
    data: {
        form: {
            name: "",
            phone: "",
            position: "",
            jersey_number: "",
            message: ""
        }
    },
    onInput(event) {
        const field = event.currentTarget.dataset.field;
        this.setData({ [`form.${field}`]: event.detail.value });
    },
    async submit() {
        if (!this.data.form.name) {
            wx.showToast({ title: "请填写姓名", icon: "none" });
            return;
        }
        await (0, request_1.request)("/join-requests", "POST", this.data.form);
        wx.showToast({ title: "已提交", icon: "success" });
        wx.switchTab({ url: "/pages/index/index" });
    }
});
