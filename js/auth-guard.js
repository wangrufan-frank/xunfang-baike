(function () {
    'use strict';

    document.documentElement.classList.add('auth-pending');

    var script = document.currentScript;
    var root = script ? (script.getAttribute('data-root') || '') : '';
    var auth = window.XunfangAuth;
    var config = window.XunfangAuthConfig;

    if (auth.hasSession(document.cookie, config)) {
        document.documentElement.classList.remove('auth-pending');
        return;
    }

    var redirect = location.pathname + location.search + location.hash;
    location.replace(root + 'auth.html?redirect=' + encodeURIComponent(redirect));
}());
