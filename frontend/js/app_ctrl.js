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

  $scope.editProfile = function() {
    var d = $modal.open({
        templateUrl: 'templates/users/profile.html',
        controller: 'UsersProfileCtrl',
        backdrop: true
    });
  };

}]);
