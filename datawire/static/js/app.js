var aleph = angular.module('aleph', ['ngRoute', 'ngAnimate', 'angular-loading-bar', 'ui.bootstrap',
                                     'debounce', 'truncate', 'infinite-scroll']);

aleph.config(['$routeProvider', '$locationProvider', 'cfpLoadingBarProvider',
    function($routeProvider, $locationProvider, cfpLoadingBarProvider) {

  cfpLoadingBarProvider.includeSpinner = false;

  $routeProvider.when('/', {
    templateUrl: 'index.html',
    controller: 'IndexCtrl'
  });

  $routeProvider.when('/lists/new', {
    templateUrl: 'lists_new.html',
    controller: 'ListsNewCtrl',
    loginRequired: true
  });

  $routeProvider.when('/lists/:id', {
    templateUrl: 'lists_edit.html',
    controller: 'ListsEditCtrl',
    loginRequired: true
  });

  $routeProvider.when('/lists/:id/entities', {
    templateUrl: 'lists_entities.html',
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


aleph.directive('entityIcon', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'category': '='
    },
    templateUrl: 'entity_icon.html',
    link: function (scope, element, attrs, model) {
    }
  };
}]);
