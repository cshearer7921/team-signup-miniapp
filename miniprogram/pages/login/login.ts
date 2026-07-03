import { request, setToken } from "../../utils/request";

Page({
  async login() {
    try {
      const wxLogin = await wx.login();
      const res = await request<{ access_token: string }>("/auth/wechat-login", "POST", {
        code: wxLogin.code,
        nickname: "微信用户"
      });
      setToken(res.access_token);
      wx.switchTab({ url: "/pages/index/index" });
    } catch (error) {
      wx.showToast({ title: "登录失败", icon: "error" });
      console.error(error);
    }
  }
});
