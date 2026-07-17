// js/nav.js
(function() {
  var MODULES = [
    { name: '装备介绍', path: 'zhuangbei/index.html',  emoji: '🛡️' },
    { name: '巡防勤务', path: 'qinwu/index.html',      emoji: '📋' },
    { name: '警务训练', path: 'xunlian/index.html',    emoji: '⚔️' },
    { name: '警情处置', path: 'jingqing/index.html',    emoji: '🚨' },
    { name: '法条规范', path: 'fagui/index.html',       emoji: '📕' },
    { name: '入门指南', path: 'rumen/index.html',       emoji: '🎓' },
    { name: '走访送教', path: 'zoufang/index.html',     emoji: '🏫' },
    { name: '本月精选', path: 'meiyueyixue/index.html', emoji: '⭐', special: true }
  ];
  var THEMES = [
    { value: 'warm-police-blue', label: '暖警蓝' },
    { value: 'classic-warm-brown', label: '经典暖棕' },
    { value: 'daylight', label: '日间浅色' },
    { value: 'night', label: '夜间深色' }
  ];
  var rootPrefix = '';

  function themeSelectorHtml() {
    var options = THEMES.map(function(theme) {
      return '<button type="button" class="theme-option" role="menuitemradio" '
        + 'data-theme-option="' + theme.value + '" aria-checked="false">'
        + '<span class="theme-swatch" aria-hidden="true"></span>' + theme.label + '</button>';
    }).join('');

    return '<div class="theme-selector">'
      + '<button type="button" class="theme-toggle" aria-label="选择网站外观" '
      + 'aria-haspopup="true" aria-expanded="false" aria-controls="theme-menu">外观</button>'
      + '<div class="theme-menu" id="theme-menu" role="menu" aria-label="网站外观">'
      + options + '</div>'
      + '</div>';
  }

  function renderNav() {
    var path = window.location.pathname.replace(/\\/g, '/');

    // 通过路径是否包含已知模块目录名判断深度
    var moduleDirs = MODULES.map(function(m) {
      return m.path.replace(/\/index\.html$/, '');
    }).filter(function(d) { return d !== 'index.html'; });
    var depth = moduleDirs.some(function(d) { return path.indexOf('/' + d + '/') !== -1; }) ? 1 : 0;
    rootPrefix = depth === 0 ? '' : '../';

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
      var cls = (m.special ? 'monthly-link' : '') + (isActive ? ' active' : '');
      var clsStr = cls.trim();
      return '<a href="' + href + '"' + (clsStr ? ' class="' + clsStr + '"' : '') + '>'
           + m.emoji + ' ' + m.name + '</a>';
    }).join('');

    return '<nav class="topnav">' +
      '<div class="logo">🛡️ 巡防百科</div>' +
      '<button class="hamburger" aria-label="菜单" aria-expanded="false">☰</button>' +
      '<div class="nav-links">' + linksHtml + themeSelectorHtml()
      + '<button type="button" class="logout-button">退出登录</button></div>' +
      '</nav>';
  }

  function updateThemeSelection(theme) {
    var options = document.querySelectorAll('[data-theme-option]');
    for (var i = 0; i < options.length; i += 1) {
      options[i].setAttribute('aria-checked', options[i].getAttribute('data-theme-option') === theme ? 'true' : 'false');
    }
  }

  function setupNav() {
    var nav = document.querySelector('.topnav');
    if (!nav) return;

    var hamburger = nav.querySelector('.hamburger');
    var navLinks = nav.querySelector('.nav-links');
    var selector = nav.querySelector('.theme-selector');
    var toggle = nav.querySelector('.theme-toggle');
    var menu = nav.querySelector('.theme-menu');
    var themeApi = window.XunfangTheme;
    var logout = nav.querySelector('.logout-button');

    if (themeApi) updateThemeSelection(themeApi.get());

    hamburger.addEventListener('click', function() {
      var open = navLinks.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    logout.addEventListener('click', window.XunfangLogout);

    toggle.addEventListener('click', function() {
      var open = selector.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    menu.addEventListener('click', function(event) {
      var option = event.target.closest('[data-theme-option]');
      if (!option || !themeApi) return;
      var theme = option.getAttribute('data-theme-option');
      window.XunfangTheme.set(theme);
      updateThemeSelection(theme);
      selector.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    });

    document.addEventListener('click', function(event) {
      if (!selector.contains(event.target)) {
        selector.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });

    nav.addEventListener('keydown', function(event) {
      if (event.key === 'Escape') {
        selector.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  window.XunfangLogout = function() {
    document.cookie = window.XunfangAuth.buildExpiredCookie(
        window.XunfangAuthConfig,
        window.location.protocol === 'https:'
    );
    window.location.replace(rootPrefix + 'auth.html');
  };

  // 注入导航
  var placeholder = document.getElementById('nav-placeholder');
  if (placeholder) {
    placeholder.outerHTML = renderNav();
    setupNav();
  }
})();
