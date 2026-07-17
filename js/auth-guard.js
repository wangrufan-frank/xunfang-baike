(function() {
  var VALID = 'f774779300ad6e9cfe4a14160c4b7ddb1b7b3efbdc3a66c706627b821367a53e';
  var COOKIE = 'xunfang_auth';

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : '';
  }

  if (getCookie(COOKIE) !== VALID) {
    var parts = location.pathname.replace(/^\//, '').split('/');
    var prefix = parts.length > 1 ? '../' : '';
    location.replace(prefix + 'auth.html?redirect=' + encodeURIComponent(location.pathname.replace(/^\//, '')));
  }
})();
