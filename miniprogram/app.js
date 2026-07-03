"use strict";
App({
    globalData: {
        apiBaseUrl: "https://cshearer.bbroot.com/api",
        token: wx.getStorageSync("token") || ""
    }
});
