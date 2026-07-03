App<IAppOption>({
  globalData: {
    apiBaseUrl: "https://你的域名/api",
    token: wx.getStorageSync("token") || ""
  }
});
