
angular.module('ngView', [], function($routeProvider, $locationProvider) {
  $routeProvider.when('/status', {
    templateUrl: '/static/partials/book.html',
    controller: StatusCntl
  });

  $locationProvider.html5Mode(true);
});

function StatusCntl($scope, $routeParams) {
  $scope.name = "StatusCntl";
  $scope.params = $routeParams;
}

function NavigationCntl($scope, $routeParams, $http) {
    $http.get('/api/1/sessions').success(function(data) {
        console.log(data);
        $scope.session = data;
    });
}
