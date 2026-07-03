"use strict";
Page({
    copyAdminUrl() {
        wx.setClipboardData({
            data: "https://cshearer.bbroot.com/admin-ui"
        });
    }
});
