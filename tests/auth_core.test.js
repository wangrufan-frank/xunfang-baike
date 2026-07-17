const test = require('node:test');
const assert = require('node:assert/strict');
const auth = require('../js/auth-core.js');
const config = require('../js/auth-config.js');

test('hashes username and password with an unambiguous separator', async () => {
    const digest = await auth.digestCredentials('demo', 'value');
    assert.equal(digest, await auth.sha256('demo:value'));
});

test('accepts the configured replacement password digest', async () => {
    assert.equal(
        await auth.digestCredentials('xunfang', 'XFbk150225'),
        config.digest
    );
    assert.notEqual(
        await auth.digestCredentials('xunfang', 'xunfang'),
        config.digest
    );
});

test('accepts only same-origin redirects', () => {
    const origin = 'https://www.xunfangbk.cn';
    assert.equal(auth.sanitizeRedirect('/kaohe/index.html?q=1#top', origin), '/kaohe/index.html?q=1#top');
    for (const value of ['https://example.com/', '//example.com/', 'javascript:alert(1)', '%%%']) {
        assert.equal(auth.sanitizeRedirect(value, origin), '/index.html');
    }
});

test('session cookie lasts one day and expires cleanly', () => {
    assert.match(auth.buildSessionCookie(config, true), /Max-Age=86400; Path=\/; SameSite=Lax; Secure/);
    assert.match(auth.buildExpiredCookie(config, false), /Max-Age=0; Path=\/; SameSite=Lax/);
});

test('session requires the exact configured token', () => {
    assert.equal(auth.hasSession('other=1; xunfang_auth=' + config.digest, config), true);
    assert.equal(auth.hasSession('xunfang_auth=wrong', config), false);
});
