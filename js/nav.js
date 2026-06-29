// js/nav.js
(function() {
  var MODULES = [
    { name: '装备介绍', path: 'zhuangbei/index.html',  emoji: '🛡️' },
    { name: '巡防勤务', path: 'qinwu/index.html',      emoji: '📋' },
    { name: '警务训练', path: 'xunlian/index.html',    emoji: '⚔️' },
    { name: '警情处置', path: 'jingqing/index.html',    emoji: '🚨' },
    { name: '法条规范', path: 'fagui/index.html',       emoji: '📕' },
    { name: '走访送教', path: 'zoufang/index.html',     emoji: '🏫' }
  ];

  function renderNav() {
    var path = window.location.pathname.replace(/\\/g, '/');

    // 通过路径是否包含已知模块目录名判断深度
    var moduleDirs = MODULES.map(function(m) {
      return m.path.replace(/\/index\.html$/, '');
    }).filter(function(d) { return d !== 'index.html'; });
    var depth = moduleDirs.some(function(d) { return path.indexOf('/' + d + '/') !== -1; }) ? 1 : 0;

    var linksHtml = MODULES.map(function(m) {
      var href = (depth === 0) ? m.path : ('../' + m.path);
      var moduleDir = m.path.replace(/\/index\.html$/, '');
      var isActive;
      if (moduleDir === 'index.html') {
        // 首页 active：路径不以任何模块目录结尾
        isActive = !moduleDirs.some(function(d) {
          return path.indexOf('/' + d + '/') !== -1 || path.endsWith('/' + d);
        });
      } else {
        isActive = path.indexOf('/' + moduleDir + '/') !== -1
               || path.endsWith('/' + moduleDir);
      }
      return '<a href="' + href + '"' + (isActive ? ' class="active"' : '') + '>'
           + m.emoji + ' ' + m.name + '</a>';
    }).join('');

    return '<nav class="topnav">' +
      '<div class="logo">🛡️ 巡防百科</div>' +
      '<button class="hamburger" aria-label="菜单">☰</button>' +
      '<div class="nav-links">' + linksHtml + '</div>' +
      '</nav>';
  }

  // 注入导航
  var placeholder = document.getElementById('nav-placeholder');
  if (placeholder) {
    placeholder.outerHTML = renderNav();
  }
})();
