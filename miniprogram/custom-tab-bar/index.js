Component({
  data: {
    selected: 0
  },
  methods: {
    switchTab(e) {
      var index = e.currentTarget.dataset.index;
      var path = e.currentTarget.dataset.path;
      if (this.data.selected === index) return;
      wx.switchTab({ url: path });
    }
  }
});
