// js/monthly-hero.js
(function() {
  if (typeof monthlyData === 'undefined') return;

  var placeholder = document.getElementById('monthly-hero-placeholder');
  if (!placeholder) return;

  var currentKey = monthlyData.current;
  var article = monthlyData.articles[currentKey];
  if (!article) return;

  var parts = currentKey.split('-');
  var label = parts[0] + '年' + parseInt(parts[1]) + '月 · 每月一学';

  var html =
    '<div class="monthly-hero">' +
      '<div class="monthly-hero-inner">' +
        '<div class="hero-label">' + label + '</div>' +
        '<div class="hero-theme">' + article.theme + '</div>' +
        '<div class="hero-summary">' + article.summary + '</div>' +
        '<a href="meiyueyixue/index.html" class="hero-link">查看全文 →</a>' +
      '</div>' +
    '</div>';

  placeholder.outerHTML = html;
})();
