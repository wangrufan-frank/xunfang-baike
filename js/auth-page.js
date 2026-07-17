(function () {
    'use strict';

    var auth = window.XunfangAuth;
    var config = window.XunfangAuthConfig;
    var form = document.getElementById('login-form');
    var usernameInput = document.getElementById('username');
    var passwordInput = document.getElementById('password');
    var toggle = document.getElementById('toggle-password');
    var submit = document.getElementById('submit');
    var error = document.getElementById('error');
    var invalidMessage = '账号或密码错误';

    function showError(message) {
        error.textContent = message;
    }

    function hasWebCrypto() {
        return window.crypto && window.crypto.subtle && window.TextEncoder;
    }

    toggle.addEventListener('click', function () {
        var reveal = passwordInput.type === 'password';
        passwordInput.type = reveal ? 'text' : 'password';
        toggle.setAttribute('aria-pressed', reveal ? 'true' : 'false');
        toggle.textContent = reveal ? '隐藏密码' : '显示密码';
        passwordInput.focus();
    });

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        if (!hasWebCrypto()) {
            showError('当前浏览器不支持安全验证，请更换现代浏览器。');
            return;
        }

        var username = usernameInput.value.trim();
        var password = passwordInput.value;
        submit.disabled = true;
        showError('');

        try {
            var digest = await auth.digestCredentials(username, password);
            if (username !== config.username || digest !== config.digest) {
                showError(invalidMessage);
                passwordInput.value = '';
                passwordInput.focus();
                return;
            }

            document.cookie = auth.buildSessionCookie(
                config,
                location.protocol === 'https:'
            );
            var redirect = new URLSearchParams(location.search).get('redirect') || '/index.html';
            var target = auth.sanitizeRedirect(redirect, location.origin);
            location.replace(target);
        } catch (caught) {
            showError('当前浏览器不支持安全验证，请更换现代浏览器。');
        } finally {
            submit.disabled = false;
        }
    });
}());
