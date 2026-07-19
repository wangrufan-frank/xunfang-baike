// js/main.js

document.addEventListener('DOMContentLoaded', function() {
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

  // ===================================================================
  // 学习型页面交互 (Learning Page Interactions)
  // ===================================================================

  // Helper: expand parent <details> if collapsed, then scroll to target
  function expandAndScrollTo(target) {
    if (!target) return;
    var parentDetails = target.closest('details');
    if (parentDetails && !parentDetails.hasAttribute('open')) {
      parentDetails.setAttribute('open', '');
    }
    // Small delay to let the browser render the newly-expanded content
    setTimeout(function() {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 80);
  }

  // 1. Expand/Collapse All toggle
  var expandAllBtn = document.querySelector('.expand-all-btn');
  var learningSections = document.querySelectorAll('.learning-section');

  if (expandAllBtn && learningSections.length > 0) {
    var allExpanded = false;
    expandAllBtn.addEventListener('click', function() {
      allExpanded = !allExpanded;
      learningSections.forEach(function(details) {
        if (allExpanded) {
          details.setAttribute('open', '');
        } else {
          details.removeAttribute('open');
        }
      });
      expandAllBtn.textContent = allExpanded ? '收起全部' : '展开全部';
    });
  }

  // 2. Hash-based auto-expand on page load
  if (window.location.hash) {
    var hashTarget = document.querySelector(window.location.hash);
    if (hashTarget) {
      expandAndScrollTo(hashTarget);
    }
  }

  // 3. TOC click handler: expand collapsed parent <details> then scroll
  var tocLinks = document.querySelectorAll('.article-toc a[href^="#"]');

  tocLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      var hash = this.getAttribute('href');
      if (!hash) return;
      var target = document.querySelector(hash);
      if (target) {
        e.preventDefault();
        expandAndScrollTo(target);
        // Update URL hash without triggering native jump
        history.pushState(null, null, hash);
        // Update active styling
        tocLinks.forEach(function(l) { l.classList.remove('active'); });
        this.classList.add('active');
      }
    });
  });

  // 4. IntersectionObserver: highlight active TOC item on scroll
  (function() {
    var articleContent = document.querySelector('.article-content');
    var tocNav = document.querySelector('.article-toc');
    if (!articleContent || !tocNav) return;
    if (typeof IntersectionObserver === 'undefined') return;

    var headings = articleContent.querySelectorAll('h2[id], h3[id]');
    if (headings.length === 0) return;

    // Build mapping: heading id -> TOC anchor
    var tocAnchors = {};
    tocNav.querySelectorAll('a[href^="#"]').forEach(function(a) {
      var id = a.getAttribute('href').slice(1);
      if (id) tocAnchors[id] = a;
    });

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting && tocAnchors[entry.target.id]) {
          Object.values(tocAnchors).forEach(function(a) {
            a.classList.remove('active');
          });
          tocAnchors[entry.target.id].classList.add('active');
        }
      });
    }, { rootMargin: '-80px 0px -60% 0px' });

    headings.forEach(function(h) { observer.observe(h); });
  })();
});
