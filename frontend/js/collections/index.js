var loadCollections = ['$http', '$q', '$location', function($http, $q, $location) {
  var params = {limit: 100}, dfd = $q.defer();
  $http.get('/api/1/collections', {params: params}).then(function(res) {
    dfd.resolve(res.data);
  });
  return dfd.promise;
}];

datawire.controller('CollectionsIndexCtrl', ['$scope', 'collections', function($scope, collections) {
  $scope.collections = collections;
}]);
