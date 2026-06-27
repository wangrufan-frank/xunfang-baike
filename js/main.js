// js/main.js
document.addEventListener('DOMContentLoaded', function() {
  // 汉堡菜单切换（使用事件委托，因为 nav 是 JS 动态注入的）
  document.addEventListener('click', function(e) {
    if (e.target.closest('.hamburger')) {
      var navLinks = document.querySelector('.nav-links');
      if (navLinks) navLinks.classList.toggle('open');
    }
  });

  // 搜索：按页面类型分派
  var searchInput = document.querySelector('.search-bar input');
  if (!searchInput) return;

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
      return;
    }
  });
});
