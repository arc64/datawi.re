var datawire = angular.module('datawire', ['ngRoute', 'ngAnimate', 'angular-loading-bar', 'ui.bootstrap',
                                           'debounce', 'truncate', 'infinite-scroll']);

datawire.config(['$routeProvider', '$locationProvider', 'cfpLoadingBarProvider',
    function($routeProvider, $locationProvider, cfpLoadingBarProvider) {

  cfpLoadingBarProvider.includeSpinner = false;

  $routeProvider.when('/', {
    templateUrl: 'index.html',
    controller: 'IndexCtrl'
  });

  $routeProvider.when('/lists/new', {
    templateUrl: 'lists/new.html',
    controller: 'ListsNewCtrl',
    loginRequired: true
  });

  $routeProvider.when('/lists/:id', {
    templateUrl: 'lists/edit.html',
    controller: 'ListsEditCtrl',
    loginRequired: true
  });

  $routeProvider.when('/lists/:id/entities', {
    templateUrl: 'lists/entities.html',
    controller: 'ListsEntitiesCtrl',
    reloadOnSearch: false,
    loginRequired: true
  });

  $routeProvider.otherwise({
    redirectTo: '/',
    loginRequired: false
  });

  $locationProvider.html5Mode(true);
}]);


datawire.directive('entityIcon', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'category': '='
    },
    templateUrl: 'entities/icon.html',
    link: function (scope, element, attrs, model) {
    }
  };
}]);
