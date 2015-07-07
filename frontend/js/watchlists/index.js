var loadWatchlists = ['$http', '$q', '$location', function($http, $q, $location) {
  var params = {limit: 100}, dfd = $q.defer();
  $http.get('/api/1/watchlists', {params: params}).then(function(res) {
    dfd.resolve(res.data);
  });
  return dfd.promise;
}];

datawire.controller('WatchlistsIndexCtrl', ['$scope', 'watchlists', function($scope, watchlists) {
  $scope.watchlists = watchlists;
}]);
