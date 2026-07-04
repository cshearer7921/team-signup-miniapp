import { MINIAPP_BUILD_TIME } from "./utils/version";

App<IAppOption>({
  globalData: {
    apiBaseUrl: "https://cshearer.bbroot.com/api",
    token: wx.getStorageSync("token") || "",
    buildTime: MINIAPP_BUILD_TIME
  }
});
