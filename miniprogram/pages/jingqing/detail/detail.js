Page({
  onLoad: function() {
    wx.showToast({
      title: '内容整改中',
      icon: 'none'
    });
    wx.switchTab({ url: '/pages/jingqing/index/index' });
  }
});
