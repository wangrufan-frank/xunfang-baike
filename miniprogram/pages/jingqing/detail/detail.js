var articles = require('../../../data/jingqing.js');

function findArticle(id) {
  for (var i = 0; i < articles.length; i++) {
    if (articles[i].id === id) return articles[i];
  }
  return null;
}

Page({
  data: { article: {}, prevTitle: '', nextTitle: '' },
  onLoad: function(opts) {
    var a = findArticle(opts.id);
    if (!a) { wx.showToast({ title: '文章未找到', icon: 'none' }); return; }

    var steps = (a.steps || []).map(function(s) {
      var lines = (s.content || '').split('\n').filter(function(l) { return l.trim(); });
      return Object.assign({}, s, {
        _expanded: false,
        _expandLabel: s.title || '展开详情',
        _contentLines: lines
      });
    });

    var prevTitle = '', nextTitle = '';
    if (a.prevId) { var p = findArticle(a.prevId); if (p) prevTitle = p.title; }
    if (a.nextId) { var n = findArticle(a.nextId); if (n) nextTitle = n.title; }

    this.setData({
      article: Object.assign({}, a, { steps: steps }),
      prevTitle: prevTitle,
      nextTitle: nextTitle
    });
  },
  onExpand: function(e) {
    var idx = e.currentTarget.dataset.index;
    var steps = this.data.article.steps;
    steps[idx]._expanded = !steps[idx]._expanded;
    this.setData({ 'article.steps': steps });
  }
});
