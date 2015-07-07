datawire.controller('AppCtrl', ['$scope', '$rootScope', '$location', '$route', '$http', '$modal', '$q',
                                'Flash', 'Session',
  function($scope, $rootScope, $location, $route, $http, $modal, $q, Flash, Session) {
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
  });

  $scope.logoutSession = function() {
    Session.logout(function(session) {
      $scope.session = session;
    });
  };

  $scope.editProfile = function() {
    $http.get('/api/1/users/' + $scope.session.user.login).success(function(user) {
      var d = $modal.open({
          templateUrl: 'templates/users/profile.html',
          controller: 'UsersProfileCtrl',
          backdrop: true,
          resolve: {
            user: function() { return user; },
            session: function() { return $scope.session; }
          }
      });
    });
  };

}]);
