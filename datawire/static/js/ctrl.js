
aleph.controller('AppCtrl', ['$scope', '$rootScope', '$location', '$route', '$http', '$modal', '$q',
                             'Flash', 'Session', 'Query', 'QueryContext',
  function($scope, $rootScope, $location, $route, $http, $modal, $q, Flash, Session, Query, QueryContext) {
  $scope.session = {logged_in: false};
  $scope.flash = Flash;

  Session.get(function(session) {
    $scope.session = session;
  });

  $rootScope.$on("$routeChangeStart", function (event, next, current) {
    Session.get(function(session) {
      if (next.$$route && next.$$route.loginRequired && !session.logged_in) {
        $location.search({});
        $location.path('/');
      }
    });
    $scope.query.state = Query.load();
  });

  $scope.editProfile = function() {
    var d = $modal.open({
        templateUrl: 'profile.html',
        controller: 'ProfileCtrl',
        backdrop: true
    });
  };

}]);


aleph.controller('IndexCtrl', ['$scope', function($scope) {

}]);



aleph.controller('ProfileCtrl', ['$scope', '$location', '$modalInstance', '$http', 'Session',
  function($scope, $location, $modalInstance, $http, Session) {
  $scope.user = {};
  $scope.session = {};

  Session.get(function(session) {
    $scope.user = session.user;
    $scope.session = session;
  });

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };

  $scope.update = function(form) {
    var res = $http.post('/api/1/users/' + $scope.user.id, $scope.user);
    res.success(function(data) {
      $scope.user = data;
      $scope.session.user = data;
      $modalInstance.dismiss('ok');
    });
  };  
}]);
