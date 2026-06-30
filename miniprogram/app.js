App({
  onLaunch() {
    var VALID = 'c252bf49e6766b2ea0f46d6ec62f6588a12ee942d363f17cfe4785d0cc75d5fb';
    var COOKIE_KEY = 'xunfang_auth';
    var val = wx.getStorageSync(COOKIE_KEY);
    var isAuthPage = getCurrentPages().length > 0
      && getCurrentPages()[0].route === 'pages/auth/auth';

    if (!isAuthPage && val !== VALID) {
      wx.reLaunch({ url: '/pages/auth/auth' });
    }
  }
});
