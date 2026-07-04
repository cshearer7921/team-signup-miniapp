import { request } from "../../utils/request";

Page({
  data: {
    submitting: false,
    form: {
      title: "",
      opponent: "",
      location: "",
      date: "",
      time: "",
      capacity: "",
      description: ""
    }
  },
  onInput(event: WechatMiniprogram.Input) {
    const field = event.currentTarget.dataset.field;
    this.setData({ [`form.${field}`]: event.detail.value });
  },
  onDateChange(event: WechatMiniprogram.PickerChange) {
    this.setData({ "form.date": event.detail.value });
  },
  onTimeChange(event: WechatMiniprogram.PickerChange) {
    this.setData({ "form.time": event.detail.value });
  },
  async submit() {
    const form = this.data.form;
    if (!form.title || !form.location || !form.date || !form.time) {
      wx.showToast({ title: "请填写必填项", icon: "none" });
      return;
    }
    const capacity: number | null = form.capacity ? Number(form.capacity) : null;
    if (capacity !== null && (!Number.isFinite(capacity) || capacity <= 0)) {
      wx.showToast({ title: "人数上限不正确", icon: "none" });
      return;
    }
    this.setData({ submitting: true });
    try {
      await request("/matches", "POST", {
        title: form.title,
        opponent: form.opponent || null,
        location: form.location,
        start_time: `${form.date}T${form.time}:00`,
        capacity,
        description: form.description || null,
        status: "open"
      });
      wx.showToast({ title: "已发布", icon: "success" });
      this.setData({
        form: { title: "", opponent: "", location: "", date: "", time: "", capacity: "", description: "" }
      });
      wx.switchTab({ url: "/pages/index/index" });
    } catch (error) {
      wx.showToast({ title: "发布失败", icon: "none" });
      console.error(error);
    } finally {
      this.setData({ submitting: false });
    }
  }
});
