Component({
  data: {
    statusBarHeight: 20
  },
  lifetimes: {
    attached: function() {
      var sys = wx.getSystemInfoSync();
      this.setData({ statusBarHeight: sys.statusBarHeight });
    }
  }
});
