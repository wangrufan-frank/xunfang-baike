// js/monthly-hero.js
(function() {
  function getArchiveEntries(data, limit) {
    if (!data || !data.articles) return [];
    return Object.keys(data.articles)
      .filter(function(key) { return key !== data.current; })
      .sort()
      .reverse()
      .slice(0, limit)
      .map(function(key) {
        var article = data.articles[key];
        return { key: key, theme: article.theme, file: article.file || (key + '.html') };
      });
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { getArchiveEntries: getArchiveEntries };
  }
  if (typeof document === 'undefined') return;
  if (typeof monthlyData === 'undefined') return;

  var placeholder = document.getElementById('monthly-hero-placeholder');
  if (!placeholder) return;

  var currentKey = monthlyData.current;
  var article = monthlyData.articles[currentKey];
  if (!article) return;

  var parts = currentKey.split('-');
  var label = parts[0] + '年' + parseInt(parts[1]) + '月 · 每月一学';

  var archiveEntries = getArchiveEntries(monthlyData, 3);
  var currentHtml =
    '<div class="hero-label">' + label + '</div>' +
    '<div class="hero-theme">' + article.theme + '</div>' +
    '<div class="hero-summary">' + article.summary + '</div>' +
    '<a href="meiyueyixue/index.html" class="hero-link">查看全文 →</a>';
  var archiveHtml = archiveEntries.length
    ? archiveEntries.map(function(entry) {
        return '<a class="monthly-archive-item" href="meiyueyixue/' + entry.file + '">' +
          '<span>' + entry.key.replace('-', '年') + '月</span>' +
          '<strong>' + entry.theme + '</strong></a>';
      }).join('')
    : '<p class="monthly-archive-empty">暂无往期内容</p>';

  var html = '<section class="monthly-hero" aria-label="每月一学">' +
    '<div class="monthly-hero-grid">' +
      '<div class="monthly-current">' + currentHtml + '</div>' +
      '<aside class="monthly-archive"><div class="monthly-archive-heading">' +
        '<strong>往期回顾</strong><span>按月归档</span></div>' + archiveHtml +
        '<a class="monthly-archive-all" href="meiyueyixue/index.html#archiveGrid">查看全部往期 →</a>' +
      '</aside>' +
    '</div></section>';

  placeholder.outerHTML = html;
})();
