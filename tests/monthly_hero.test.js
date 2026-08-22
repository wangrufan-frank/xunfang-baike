const test = require('node:test');
const assert = require('node:assert/strict');
const { getArchiveEntries, renderMonthlyHero } = require('../js/monthly-hero.js');

test('archive excludes current issue, sorts newest first, and limits results', () => {
  const data = {
    current: '2026-08',
    articles: {
      '2026-06': { theme: '六月', file: '2026-06.html' },
      '2026-08': { theme: '八月', file: 'index.html' },
      '2026-07': { theme: '七月', file: '2026-07.html' },
      '2026-05': { theme: '五月', file: '2026-05.html' }
    }
  };
  assert.deepEqual(
    getArchiveEntries(data, 2).map((entry) => entry.key),
    ['2026-07', '2026-06']
  );
});

test('archive returns an empty list when no past issue exists', () => {
  const data = { current: '2026-08', articles: { '2026-08': { theme: '八月' } } };
  assert.deepEqual(getArchiveEntries(data, 3), []);
});

test('renderer creates the current issue plus the three newest archived links', () => {
  const placeholder = {};
  const document = { getElementById: () => placeholder };
  const data = {
    current: '2026-08',
    articles: {
      '2026-05': { theme: '五月', file: '2026-05.html' },
      '2026-06': { theme: '六月', file: '2026-06.html' },
      '2026-07': { theme: '七月', file: '2026-07.html' },
      '2026-08': { theme: '八月', summary: '本期内容' },
      '2026-09': { theme: '九月', file: '2026-09.html' }
    }
  };

  renderMonthlyHero(data, document);

  assert.match(placeholder.outerHTML, /class="monthly-hero-grid"/);
  assert.match(placeholder.outerHTML, /往期回顾/);
  assert.deepEqual(
    [...placeholder.outerHTML.matchAll(/class="monthly-archive-item" href="([^"]+)"/g)].map((match) => match[1]),
    ['meiyueyixue/2026-09.html', 'meiyueyixue/2026-07.html', 'meiyueyixue/2026-06.html']
  );
});

test('renderer displays an empty archive state when the current issue is the only issue', () => {
  const placeholder = {};
  const document = { getElementById: () => placeholder };
  const data = {
    current: '2026-08',
    articles: { '2026-08': { theme: '八月', summary: '本期内容' } }
  };

  renderMonthlyHero(data, document);

  assert.match(placeholder.outerHTML, /暂无往期内容/);
});
