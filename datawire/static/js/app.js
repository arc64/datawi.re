
var module = angular.module('datawire', [], function($routeProvider, $locationProvider) {
  $routeProvider.when('/profile', {
    templateUrl: '/static/partials/profile.html',
    controller: ProfileCntl
  });

  $routeProvider.when('/feed', {
    templateUrl: '/static/partials/feed.html',
    controller: FeedCntl
  });

  $locationProvider.html5Mode(true);
});

module.run(function($rootScope) {
    $rootScope.visit = function(url) {
        $window.location.href = url;
    };
});

function ProfileCntl($scope, $routeParams) {
  $scope.message = 'I am a banana!';
}

function NavigationCntl($scope, $window, $routeParams, $http) {
    $http.get('/api/1/sessions').success(function(data) {
        console.log(data);
        $scope.session = data;
    });
    $scope.visit = function(url) {
        $window.location.href = url;
    };
}

function FeedCntl($scope, $routeParams, $http) {
    $http.get('/api/1/frames').success(function(data) {
        console.log(data);
        $scope.frames = data.results;
        $scope.services = data.services;
    });
}