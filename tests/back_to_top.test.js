const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

function loadPage(scrollY = 0, reducedMotion = false) {
  const listeners = {};
  const buttons = [];
  const window = {
    location: { pathname: '/meiyueyixue/index.html' },
    scrollY,
    innerHeight: 800,
    addEventListener: (name, callback) => { listeners[name] = callback; },
    matchMedia: () => ({ matches: reducedMotion }),
    scrollTo: (options) => { window.lastScroll = options; }
  };
  const document = {
    getElementById: () => ({}),
    querySelector: () => null,
    body: { classList: { add() {} }, appendChild: (button) => buttons.push(button) },
    createElement: () => ({
      setAttribute(name, value) { this[name] = value; },
      addEventListener(name, callback) { this[name] = callback; }
    })
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../js/nav.js'), 'utf8'), { window, document });
  return { window, listeners, buttons };
}

test('button appears only after one viewport and hides again at the top', () => {
  const page = loadPage();
  assert.equal(page.buttons.length, 1);
  const button = page.buttons[0];
  assert.equal(button.type, 'button');
  assert.equal(button.hidden, true);
  page.window.scrollY = 801;
  page.listeners.scroll();
  assert.equal(button.hidden, false);
  page.window.scrollY = 0;
  page.listeners.scroll();
  assert.equal(button.hidden, true);
});

test('restored scroll position and viewport changes update visibility', () => {
  const page = loadPage(900);
  assert.equal(page.buttons[0].hidden, false);
  page.window.innerHeight = 1000;
  page.listeners.resize();
  assert.equal(page.buttons[0].hidden, true);
});

test('click returns to the top and respects reduced motion', () => {
  for (const reducedMotion of [false, true]) {
    const page = loadPage(1800, reducedMotion);
    page.buttons[0].click();
    assert.equal(page.window.lastScroll.top, 0);
    assert.equal(page.window.lastScroll.behavior, reducedMotion ? 'instant' : 'smooth');
  }
});
