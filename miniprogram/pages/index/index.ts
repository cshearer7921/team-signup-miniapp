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
      const rows = await request<any[]>("/matches");
      const matches = rows.map((item) => ({
        ...item,
        status_text: matchStatusText(item.status)
      }));
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

function matchStatusText(status?: string): string {
  const map: Record<string, string> = {
    open: "开放报名",
    finished: "已完成",
    closed: "已关闭",
    cancelled: "已取消"
  };
  return status ? map[status] || status : "-";
}
