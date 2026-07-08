// js/search.js
(function() {
  var SEARCH_INDEX_URL = 'search-index.json';
  var DEBOUNCE_MS = 200;
  var MAX_DROPDOWN_RESULTS = 8;

  var searchIndex = null;
  var debounceTimer = null;
  var dropdownEl = null;
  var searchInput = null;
  var searchBar = null;
  var loaded = false;
  var loadError = false;

  // 判断当前页面深度
  function getDepth() {
    var path = window.location.pathname.replace(/\\/g, '/');
    var dirs = path.split('/').filter(function(d) { return d && d !== 'index.html'; });
    // 如果在子目录中（路径包含模块目录），depth=1
    var moduleDirs = ['zhuangbei','qinwu','xunlian','jingqing','fagui','zoufang','meiyueyixue'];
    for (var i = 0; i < moduleDirs.length; i++) {
      if (dirs.indexOf(moduleDirs[i]) !== -1) return 1;
    }
    return 0;
  }

  function getIndexUrl() {
    var depth = getDepth();
    return (depth === 0) ? SEARCH_INDEX_URL : ('../' + SEARCH_INDEX_URL);
  }

  function getSearchPageUrl() {
    var depth = getDepth();
    return (depth === 0) ? 'search.html' : '../search.html';
  }

  // 加载索引
  function loadIndex(callback) {
    if (searchIndex) { callback(); return; }
    if (loadError) { callback(new Error('load failed')); return; }

    var xhr = new XMLHttpRequest();
    xhr.open('GET', getIndexUrl(), true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          searchIndex = JSON.parse(xhr.responseText);
          loaded = true;
          callback();
        } catch(e) {
          loadError = true;
          callback(e);
        }
      } else {
        loadError = true;
        callback(new Error('HTTP ' + xhr.status));
      }
    };
    xhr.onerror = function() {
      loadError = true;
      callback(new Error('network error'));
    };
    xhr.send();
  }

  // 匹配分数计算
  function matchScore(item, queryLower) {
    var score = 0;
    var titleLower = item.title.toLowerCase();
    var descLower = item.desc.toLowerCase();

    if (titleLower.indexOf(queryLower) !== -1) score += 5;
    if (descLower.indexOf(queryLower) !== -1) score += 1;

    if (item.tags) {
      for (var i = 0; i < item.tags.length; i++) {
        if (item.tags[i].toLowerCase().indexOf(queryLower) !== -1) { score += 3; break; }
      }
    }

    if (item.keywords) {
      for (var i = 0; i < item.keywords.length; i++) {
        if (item.keywords[i].toLowerCase().indexOf(queryLower) !== -1) { score += 3; }
      }
    }

    return score;
  }

  // 高亮匹配文本
  function highlight(text, queryLower) {
    if (!queryLower) return escapeHtml(text);
    var escaped = escapeHtml(text);
    var idx = escaped.toLowerCase().indexOf(queryLower);
    if (idx === -1) return escaped;

    var prefix = escaped.substring(0, idx);
    var match = escaped.substring(idx, idx + queryLower.length);
    var suffix = escaped.substring(idx + queryLower.length);
    return prefix + '<span class="search-highlight">' + match + '</span>' + suffix;
  }

  function escapeHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  // 执行搜索
  function doSearch(query) {
    if (!query || query.trim().length === 0) {
      closeDropdown();
      return;
    }

    if (!searchIndex) {
      loadIndex(function(err) {
        if (err) return;
        doSearch(query);
      });
      return;
    }

    var queryLower = query.trim().toLowerCase();
    var scored = [];

    for (var i = 0; i < searchIndex.length; i++) {
      var s = matchScore(searchIndex[i], queryLower);
      if (s > 0) {
        scored.push({ item: searchIndex[i], score: s });
      }
    }

    scored.sort(function(a, b) { return b.score - a.score; });

    var results = scored.slice(0, MAX_DROPDOWN_RESULTS);
    var totalCount = scored.length;

    renderDropdown(results, totalCount, queryLower, query.trim());
  }

  // 渲染下拉面板
  function renderDropdown(results, totalCount, queryLower, rawQuery) {
    if (!dropdownEl) {
      dropdownEl = document.createElement('div');
      dropdownEl.className = 'search-dropdown';
      searchBar.appendChild(dropdownEl);

      // 点击外部关闭
      document.addEventListener('click', function(e) {
        if (dropdownEl && !dropdownEl.contains(e.target) && e.target !== searchInput) {
          closeDropdown();
        }
      });
    }

    if (results.length === 0) {
      dropdownEl.innerHTML =
        '<div class="search-empty">未找到相关内容' +
        '<div class="empty-hint">试试其他关键词，如"警棍""盘查""持刀"</div>' +
        '</div>';
    } else {
      var depth = getDepth();
      var prefix = (depth === 0) ? '' : '../';

      var itemsHtml = '';
      for (var i = 0; i < results.length; i++) {
        var item = results[i].item;
        itemsHtml +=
          '<a href="' + prefix + item.path + '" class="search-result-item">' +
            '<div class="result-title">' + highlight(item.title, queryLower) + '</div>' +
            '<span class="result-module">' + escapeHtml(item.module) + '</span>' +
            '<div class="result-desc">' + highlight(item.desc, queryLower) + '</div>' +
          '</a>';
      }

      if (totalCount > MAX_DROPDOWN_RESULTS) {
        itemsHtml += '<a href="' + getSearchPageUrl() + '?q=' + encodeURIComponent(rawQuery) + '" class="search-more">查看全部 ' + totalCount + ' 条结果 →</a>';
      }

      dropdownEl.innerHTML = itemsHtml;
    }

    dropdownEl.classList.add('open');
  }

  function closeDropdown() {
    if (dropdownEl) {
      dropdownEl.classList.remove('open');
    }
  }

  // 初始化
  function init() {
    searchInput = document.querySelector('.search-bar input');
    if (!searchInput) return;

    searchBar = searchInput.parentElement;
    // 给搜索栏加 wrapper 以便定位下拉面板
    searchBar.classList.add('search-wrapper');

    // 输入事件（防抖）
    searchInput.addEventListener('input', function() {
      clearTimeout(debounceTimer);
      var query = searchInput.value;
      debounceTimer = setTimeout(function() {
        loadIndex(function(err) {
          if (err) {
            // 索引加载失败，不影响正常使用
            return;
          }
          doSearch(query);
        });
      }, DEBOUNCE_MS);
    });

    // 回车跳转搜索结果页
    searchInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        var query = searchInput.value.trim();
        if (query) {
          window.location.href = getSearchPageUrl() + '?q=' + encodeURIComponent(query);
        }
      }
      if (e.key === 'Escape') {
        closeDropdown();
      }
    });

    // 聚焦时如果输入框有内容则重新搜索
    searchInput.addEventListener('focus', function() {
      if (searchInput.value.trim()) {
        doSearch(searchInput.value);
      }
    });

    // 预加载索引
    loadIndex(function() {});
  }

  // DOM ready 后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
