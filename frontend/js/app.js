var datawire = angular.module('datawire', ['ngRoute', 'ngAnimate', 'angular-loading-bar', 'ui.bootstrap',
                                           'debounce', 'truncate', 'infinite-scroll', 'datawire.templates']);

datawire.config(['$routeProvider', '$locationProvider', 'cfpLoadingBarProvider',
    function($routeProvider, $locationProvider, cfpLoadingBarProvider) {

  cfpLoadingBarProvider.includeSpinner = false;

  $routeProvider.when('/', {
    templateUrl: 'templates/collections/index.html',
    controller: 'CollectionsIndexCtrl',
    resolve: {
      'collections': loadCollections
    }
  });

  $routeProvider.when('/collections/new', {
    templateUrl: 'templates/collections/new.html',
    controller: 'CollectionsNewCtrl',
    loginRequired: true
  });

  $routeProvider.when('/collections/:id', {
    templateUrl: 'templates/collections/edit.html',
    controller: 'CollectionsEditCtrl'
  });

  $routeProvider.when('/collections/:id/entities', {
    templateUrl: 'templates/entities/index.html',
    controller: 'EntitiesIndexCtrl',
    reloadOnSearch: false
  });

  $routeProvider.otherwise({
    redirectTo: '/',
    loginRequired: false
  });

  $locationProvider.html5Mode(true);
}]);
