const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function loadAnalytics(hostname) {
  const scripts = [];
  const document = {
    getElementById: () => null,
    createElement: () => ({ setAttribute(name, value) { this[name] = value; } }),
    head: { appendChild: (script) => scripts.push(script) }
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../js/nav.js'), 'utf8'), {
    document,
    window: { location: { hostname } }
  });
  return scripts;
}

test('public domains load the provided Umami website tracker once', () => {
  for (const hostname of ['www.xunfangbk.cn', 'xunfangbk.cn']) {
    const scripts = loadAnalytics(hostname);
    assert.equal(scripts.length, 1);
    assert.equal(scripts[0].src, 'https://cloud.umami.is/script.js');
    assert.equal(scripts[0]['data-website-id'], '29fd0aaa-5fe3-4677-9fbd-9245966cff14');
    assert.equal(scripts[0]['data-domains'], 'www.xunfangbk.cn,xunfangbk.cn');
    assert.equal(scripts[0].async, true);
  }
});

test('local previews and other hosts do not load analytics', () => {
  for (const hostname of ['localhost', '127.0.0.1', '', 'example.com']) {
    assert.equal(loadAnalytics(hostname).length, 0);
  }
});
