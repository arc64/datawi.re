var datawire = angular.module('datawire', ['ngRoute', 'ngAnimate', 'angular-loading-bar', 'ui.bootstrap',
                                           'debounce', 'truncate', 'infinite-scroll', 'datawire.templates']);

datawire.config(['$routeProvider', '$locationProvider', 'cfpLoadingBarProvider',
    function($routeProvider, $locationProvider, cfpLoadingBarProvider) {

  cfpLoadingBarProvider.includeSpinner = false;

  $routeProvider.when('/', {
    templateUrl: 'templates/watchlists/index.html',
    controller: 'WatchlistsIndexCtrl',
    resolve: {
      'watchlists': loadWatchlists
    }
  });

  $routeProvider.when('/lists/new', {
    templateUrl: 'templates/watchlists/new.html',
    controller: 'WatchlistsNewCtrl',
    loginRequired: true
  });

  $routeProvider.when('/lists/:id', {
    templateUrl: 'templates/watchlists/edit.html',
    controller: 'WatchlistsEditCtrl',
    loginRequired: true
  });

  $routeProvider.when('/lists/:id/entities', {
    templateUrl: 'templates/entities/index.html',
    controller: 'EntitiesIndexCtrl',
    reloadOnSearch: false,
    loginRequired: true
  });

  $routeProvider.otherwise({
    redirectTo: '/',
    loginRequired: false
  });

  $locationProvider.html5Mode(true);
}]);
