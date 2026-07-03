"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getToken = getToken;
exports.setToken = setToken;
exports.request = request;
function getToken() {
    return wx.getStorageSync("token") || "";
}
function setToken(token) {
    wx.setStorageSync("token", token);
    getApp().globalData.token = token;
}
function request(path, method = "GET", data) {
    const app = getApp();
    return new Promise((resolve, reject) => {
        wx.request({
            url: `${app.globalData.apiBaseUrl}${path}`,
            method: method,
            data: data,
            header: {
                "Content-Type": "application/json",
                Authorization: getToken() ? `Bearer ${getToken()}` : ""
            },
            success(res) {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(res.data);
                }
                else if (res.statusCode === 401) {
                    wx.removeStorageSync("token");
                    wx.navigateTo({ url: "/pages/login/login" });
                    reject(res.data);
                }
                else {
                    reject(res.data);
                }
            },
            fail: reject
        });
    });
}
