datawire.controller('WatchlistsNewCtrl', ['$scope', '$location', '$http', '$routeParams', 'Validation',
  function($scope, $location, $http, $routeParams, Validation, QueryContext) {
  $scope.list = {'public': false, 'new': true};

  $scope.canCreate = function() {
    return $scope.session.logged_in;
  };

  $scope.create = function(form) {
      var res = $http.post('/api/1/lists', $scope.list);
      res.success(function(data) {
        $location.path('/lists/' + data.id + '/entities');
      });
      res.error(Validation.handle(form));
  };

}]);
