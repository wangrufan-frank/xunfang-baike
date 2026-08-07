// js/changelog.js
(function() {
  function escapeHtml(str) {
    return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
  function render(updates) {
    var listEl = document.getElementById('changelog-list');
    if (!listEl) return;
    if (!updates || !updates.length) {
      listEl.innerHTML = '<div class="changelog-empty">暂无更新记录</div>';
      return;
    }
    var html = '';
    for (var i = 0; i < updates.length; i++) {
      var u = updates[i];
      html += '<div class="changelog-entry">'
        + '<div class="changelog-date">' + escapeHtml(u.date) + '</div>'
        + '<div class="changelog-title">' + escapeHtml(u.title) + '</div>'
        + '<ul class="changelog-items">';
      for (var j = 0; j < u.items.length; j++) {
        html += '<li>' + escapeHtml(u.items[j]) + '</li>';
      }
      html += '</ul></div>';
    }
    listEl.innerHTML = html;
  }
  function fail() {
    var listEl = document.getElementById('changelog-list');
    if (listEl) listEl.innerHTML = '<div class="changelog-empty">更新记录加载失败</div>';
  }
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'data/updates.json', true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      try { render(JSON.parse(xhr.responseText).updates); }
      catch (e) { fail(); }
    } else { fail(); }
  };
  xhr.onerror = fail;
  xhr.send();
})();
