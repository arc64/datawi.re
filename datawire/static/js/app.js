
angular.module('ngView', [], function($routeProvider, $locationProvider) {
  $routeProvider.when('/profile', {
    templateUrl: '/static/partials/profile.html',
    controller: ProfileCntl
  });

  $locationProvider.html5Mode(true);
});

function ProfileCntl($scope, $routeParams) {
  $scope.message = 'I am a banana!';
}

function NavigationCntl($scope, $routeParams, $http) {
    $http.get('/api/1/sessions').success(function(data) {
        console.log(data);
        $scope.session = data;
    });
}
