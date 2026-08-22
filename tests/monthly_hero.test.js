const test = require('node:test');
const assert = require('node:assert/strict');
const { getArchiveEntries } = require('../js/monthly-hero.js');

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
