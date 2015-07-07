datawire.factory('Session', ['$http', function($http) {
  var sessionDfd = null;

  var flush = function() {
    sessionDfd = null;
  };

  var logout = function(cb) {
    $http.post('/api/1/sessions/logout').then(function() {
      flush();
      get(cb);
    });
  };

  var get = function(cb) {
    if (sessionDfd === null) {
      var data = {'_': new Date()}
      sessionDfd = $http.get('/api/1/sessions', {params: data});
    }
    sessionDfd.then(function(res) {
      cb(res.data);
    });
  };

  return {
    'get': get,
    'flush': flush,
    'logout': logout
  }
}]);
