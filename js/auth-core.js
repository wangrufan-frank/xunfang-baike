(function (root, factory) {
    var auth = factory();

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = auth;
    } else {
        root.XunfangAuth = auth;
    }
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    async function sha256(text) {
        var bytes = new TextEncoder().encode(text);
        var digest = await globalThis.crypto.subtle.digest('SHA-256', bytes);

        return Array.from(new Uint8Array(digest), function (byte) {
            return byte.toString(16).padStart(2, '0');
        }).join('');
    }

    function digestCredentials(username, password) {
        return sha256(username + ':' + password);
    }

    function sanitizeRedirect(value, origin) {
        try {
            decodeURI(value);
            var target = new URL(value, origin);

            if (target.origin !== origin || (target.protocol !== 'http:' && target.protocol !== 'https:')) {
                return '/index.html';
            }

            return target.pathname + target.search + target.hash;
        } catch (error) {
            return '/index.html';
        }
    }

    function hasSession(cookieText, config) {
        return cookieText.split(';').some(function (cookie) {
            var separator = cookie.indexOf('=');
            var name = separator === -1 ? cookie.trim() : cookie.slice(0, separator).trim();
            var value = separator === -1 ? '' : cookie.slice(separator + 1);

            return name === config.cookieName && value === encodeURIComponent(config.digest);
        });
    }

    function buildSessionCookie(config, secure) {
        var cookie = config.cookieName + '=' + encodeURIComponent(config.digest)
            + '; Max-Age=' + config.maxAgeSeconds + '; Path=/; SameSite=Lax';

        return secure ? cookie + '; Secure' : cookie;
    }

    function buildExpiredCookie(config, secure) {
        var cookie = config.cookieName + '=; Max-Age=0; Path=/; SameSite=Lax';

        return secure ? cookie + '; Secure' : cookie;
    }

    return {
        sha256: sha256,
        digestCredentials: digestCredentials,
        sanitizeRedirect: sanitizeRedirect,
        hasSession: hasSession,
        buildSessionCookie: buildSessionCookie,
        buildExpiredCookie: buildExpiredCookie
    };
}));
