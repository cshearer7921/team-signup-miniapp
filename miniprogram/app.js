"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const version_1 = require("./utils/version");
App({
    globalData: {
        apiBaseUrl: "https://cshearer.bbroot.com/api",
        token: wx.getStorageSync("token") || "",
        buildTime: version_1.MINIAPP_BUILD_TIME
    }
});
