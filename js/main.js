// js/main.js

// ── 认证守卫 ──
(function(){
  var COOKIE = 'xunfang_auth';
  var VALID = 'c252bf49e6766b2ea0f46d6ec62f6588a12ee942d363f17cfe4785d0cc75d5fb';
  var isAuthPage = location.pathname.endsWith('/auth.html') || location.pathname === '/auth.html';
  if (isAuthPage) return;
  var val = document.cookie.split('; ').reduce(function(acc, c) {
    var kv = c.split('='); acc[kv[0]] = kv.slice(1).join('='); return acc;
  }, {})[COOKIE];
  if (val !== VALID) {
    var redir = encodeURIComponent(location.pathname.replace(/^.*[\\\/]/, '') + location.search);
    location.replace('auth.html?redirect=' + redir);
  }
})();

document.addEventListener('DOMContentLoaded', function() {
  // 汉堡菜单切换（使用事件委托，因为 nav 是 JS 动态注入的）
  document.addEventListener('click', function(e) {
    if (e.target.closest('.hamburger')) {
      var navLinks = document.querySelector('.nav-links');
      if (navLinks) navLinks.classList.toggle('open');
    }
  });

  // 搜索：按页面类型分派（仅首页和列表页有效）
  var searchInput = document.querySelector('.search-bar input');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      var query = this.value.toLowerCase().trim();

      // 首页：过滤模块卡片
      var moduleCards = document.querySelectorAll('.module-card');
      if (moduleCards.length > 0) {
        moduleCards.forEach(function(card) {
          var text = (card.textContent || '').toLowerCase();
          card.style.display = text.includes(query) ? '' : 'none';
        });
        return;
      }

      // 列表页：过滤 list-item 链接，联动隐藏空分组标题
      var listItems = document.querySelectorAll('.list-page .list-item');
      if (listItems.length > 0) {
        listItems.forEach(function(item) {
          var text = (item.textContent || '').toLowerCase();
          item.style.display = text.includes(query) ? '' : 'none';
        });

        var sections = document.querySelectorAll('.list-section-title');
        sections.forEach(function(section) {
          var allHidden = true;
          var el = section.nextElementSibling;
          while (el && !el.classList.contains('list-section-title')) {
            if (el.classList.contains('list-item') && el.style.display !== 'none') {
              allHidden = false;
            }
            el = el.nextElementSibling;
          }
          section.style.display = allHidden ? 'none' : '';
        });
      }
    });
  }

  // 折叠展开交互
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('.expand-btn');
    if (!btn) return;

    var card = btn.closest('.step-card');
    if (!card) return;

    var full = card.querySelector('.expandable-full');
    if (!full) return;

    var isOpen = full.classList.contains('open');
    if (isOpen) {
      full.classList.remove('open');
      btn.textContent = btn.getAttribute('data-expand-text') || '▸ 展开详情';
    } else {
      if (!btn.getAttribute('data-expand-text')) {
        btn.setAttribute('data-expand-text', btn.textContent);
      }
      full.classList.add('open');
      btn.textContent = '▸ 收起';
    }
  });
});
