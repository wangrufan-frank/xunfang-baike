var articles = require('../../../data/jingqing.js');

Page({
  data: { sections: [], allItems: [] },
  onShow() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 3 });
    }
  },
  onLoad() {
    var sections = [];
    var seen = {};
    articles.forEach(function(a) {
      if (!seen[a.section]) {
        seen[a.section] = { name: a.section, items: [] };
        sections.push(seen[a.section]);
      }
      seen[a.section].items.push({ id: a.id, icon: a.icon, title: a.title, desc: a.desc });
    });
    this.setData({ sections: sections, allItems: articles });
  },
  onSearch(e) {
    var q = e.detail.value.toLowerCase().trim();
    var sections = [];
    var seen = {};
    var self = this;
    this.data.allItems.forEach(function(a) {
      if (q && (a.title + a.desc).toLowerCase().indexOf(q) === -1) return;
      if (!seen[a.section]) {
        seen[a.section] = { name: a.section, items: [] };
        sections.push(seen[a.section]);
      }
      seen[a.section].items.push({ id: a.id, icon: a.icon, title: a.title, desc: a.desc });
    });
    this.setData({ sections: sections });
  }
});
