import { request } from "../../utils/request";

const statusMap: Record<string, string> = { signed_up: "报名", leave: "请假", maybe: "待定" };

Page({
  data: {
    id: 0,
    match: {} as any,
    signups: [] as any[],
    statusMap,
    statusText: "未报名"
  },
  onLoad(query) {
    this.setData({ id: Number(query.id) });
    this.load();
  },
  async load() {
    const match = await request<any>(`/matches/${this.data.id}`);
    const signups = await request<any[]>(`/matches/${this.data.id}/signups`);
    this.setData({
      match,
      signups,
      statusText: statusMap[match.my_signup_status] || "未报名"
    });
  },
  async signup(event: WechatMiniprogram.TouchEvent) {
    const status = event.currentTarget.dataset.status;
    await request(`/matches/${this.data.id}/signup`, "POST", { status });
    wx.showToast({ title: "已提交", icon: "success" });
    this.load();
  }
});
