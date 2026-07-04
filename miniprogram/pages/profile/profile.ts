import { getToken, request } from "../../utils/request";

Page({
  data: {
    token: "",
    me: {} as any,
    memberStatusText: "未申请",
    roleText: "-"
  },
  onShow() {
    this.setData({ token: getToken() });
    if (getToken()) this.loadMe();
  },
  async loadMe() {
    const me = await request<any>("/me");
    this.setData({
      me,
      memberStatusText: statusText(me.member_status),
      roleText: roleText(me.role)
    });
  },
  goLogin() {
    wx.navigateTo({ url: "/pages/login/login" });
  },
  goJoin() {
    wx.navigateTo({ url: "/pages/join-request/join-request" });
  },
  logout() {
    wx.removeStorageSync("token");
    this.setData({ token: "", me: {}, memberStatusText: "未申请", roleText: "-" });
  }
});

function statusText(status?: string): string {
  const map: Record<string, string> = {
    pending: "待审核",
    approved: "已通过",
    rejected: "已拒绝"
  };
  return status ? map[status] || status : "未申请";
}

function roleText(role?: string): string {
  const map: Record<string, string> = {
    player: "球员",
    captain: "队长",
    admin: "管理员"
  };
  return role ? map[role] || role : "-";
}
