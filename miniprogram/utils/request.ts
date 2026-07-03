type Method = "GET" | "POST" | "PATCH" | "DELETE";

export function getToken(): string {
  return wx.getStorageSync("token") || "";
}

export function setToken(token: string): void {
  wx.setStorageSync("token", token);
  getApp<IAppOption>().globalData.token = token;
}

export function request<T>(path: string, method: Method = "GET", data?: unknown): Promise<T> {
  const app = getApp<IAppOption>();
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${app.globalData.apiBaseUrl}${path}`,
      method: method as WechatMiniprogram.RequestOption["method"],
      data: data as WechatMiniprogram.IAnyObject | string | ArrayBuffer | undefined,
      header: {
        "Content-Type": "application/json",
        Authorization: getToken() ? `Bearer ${getToken()}` : ""
      },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data as T);
        } else if (res.statusCode === 401) {
          wx.removeStorageSync("token");
          wx.navigateTo({ url: "/pages/login/login" });
          reject(res.data);
        } else {
          reject(res.data);
        }
      },
      fail: reject
    });
  });
}
