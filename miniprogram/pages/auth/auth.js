Page({
  data: { pwd: '', error: '' },
  onInput(e) { this.setData({ pwd: e.detail.value, error: '' }); },
  async onSubmit() {
    var VALID = 'c252bf49e6766b2ea0f46d6ec62f6588a12ee942d363f17cfe4785d0cc75d5fb';
    var pwd = this.data.pwd.trim();
    if (!pwd) { this.setData({ error: '请输入密码' }); return; }
    var buf = new Uint8Array(await crypto.subtle.digest('SHA-256',
      new TextEncoder().encode(pwd)));
    var h = Array.from(buf).map(function(b){ return b.toString(16).padStart(2,'0'); }).join('');
    if (h !== VALID) { this.setData({ error: '密码错误', pwd: '' }); return; }
    wx.setStorageSync('xunfang_auth', h);
    wx.switchTab({ url: '/pages/zhuangbei/index/index' });
  }
});
