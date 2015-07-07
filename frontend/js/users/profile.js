datawire.controller('UsersProfileCtrl', ['$scope', '$location', '$modalInstance', '$http', 'session', 'user',
  function($scope, $location, $modalInstance, $http, session, user) {
  $scope.user = user;
  $scope.session = session;

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };

  $scope.update = function(form) {
    var res = $http.post('/api/1/users/' + $scope.user.login, $scope.user);
    res.success(function(data) {
      $scope.user = data;
      $scope.session.user = data;
      $modalInstance.dismiss('ok');
    });
  };
}]);
