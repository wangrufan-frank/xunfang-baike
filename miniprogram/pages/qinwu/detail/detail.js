Page({
  onLoad: function() {
    wx.showToast({
      title: '内容整改中',
      icon: 'none'
    });
    wx.redirectTo({ url: '/pages/qinwu/index/index' });
  }
});
