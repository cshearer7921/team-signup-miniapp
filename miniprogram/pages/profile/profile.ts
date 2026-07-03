import { getToken, request } from "../../utils/request";

Page({
  data: {
    token: "",
    me: {} as any
  },
  onShow() {
    this.setData({ token: getToken() });
    if (getToken()) this.loadMe();
  },
  async loadMe() {
    const me = await request<any>("/me");
    this.setData({ me });
  },
  goLogin() {
    wx.navigateTo({ url: "/pages/login/login" });
  },
  goJoin() {
    wx.navigateTo({ url: "/pages/join-request/join-request" });
  },
  logout() {
    wx.removeStorageSync("token");
    this.setData({ token: "", me: {} });
  }
});
