import { getToken, request } from "../../utils/request";

Page({
  data: {
    token: "",
    matches: [] as any[]
  },
  onShow() {
    this.setData({ token: getToken() });
    if (getToken()) this.loadMatches();
  },
  async loadMatches() {
    try {
      const matches = await request<any[]>("/matches");
      this.setData({ matches });
    } catch (error) {
      console.error(error);
    }
  },
  goLogin() {
    wx.navigateTo({ url: "/pages/login/login" });
  },
  goJoin() {
    wx.navigateTo({ url: "/pages/join-request/join-request" });
  },
  goCreate() {
    wx.switchTab({ url: "/pages/create-activity/create-activity" });
  },
  openMatch(event: WechatMiniprogram.TouchEvent) {
    wx.navigateTo({ url: `/pages/match-detail/match-detail?id=${event.currentTarget.dataset.id}` });
  }
});
