(function() {
  'use strict';

  var STORAGE_KEY = 'xunfang-theme';
  var DEFAULT_THEME = 'warm-police-blue';
  var THEMES = [
    'warm-police-blue',
    'classic-warm-brown',
    'daylight',
    'night'
  ];

  function isSupported(theme) {
    return THEMES.indexOf(theme) !== -1;
  }

  function readTheme() {
    try {
      var stored = window.localStorage.getItem(STORAGE_KEY);
      return isSupported(stored) ? stored : DEFAULT_THEME;
    } catch (error) {
      return DEFAULT_THEME;
    }
  }

  function set(theme) {
    var selected = isSupported(theme) ? theme : DEFAULT_THEME;
    document.documentElement.dataset.theme = selected;

    try {
      window.localStorage.setItem(STORAGE_KEY, selected);
    } catch (error) {
      // Keep the selected theme for this page even when storage is unavailable.
    }

    return selected;
  }

  window.XunfangTheme = {
    get: readTheme,
    set: set,
    themes: THEMES.slice()
  };

  document.documentElement.dataset.theme = readTheme();
})();
