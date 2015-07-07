var datawire = angular.module('datawire', ['ngRoute', 'ngAnimate', 'angular-loading-bar', 'ui.bootstrap',
                                           'debounce', 'truncate', 'infinite-scroll', 'datawire.templates']);

datawire.config(['$routeProvider', '$locationProvider', 'cfpLoadingBarProvider',
    function($routeProvider, $locationProvider, cfpLoadingBarProvider) {

  cfpLoadingBarProvider.includeSpinner = false;

  $routeProvider.when('/', {
    templateUrl: 'templates/watchlists/index.html',
    controller: 'WatchlistsIndexCtrl'
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
;datawire.controller('AppCtrl', ['$scope', '$rootScope', '$location', '$route', '$http', '$modal', '$q',
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
    console.log('FOOOO!');
    Session.logout(function(session) {
      $scope.session = session;
    });
  };

  $scope.editProfile = function() {
    var d = $modal.open({
        templateUrl: 'templates/users/profile.html',
        controller: 'UsersProfileCtrl',
        backdrop: true
    });
  };

}]);
;datawire.directive('entityIcon', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'category': '='
    },
    templateUrl: 'templates/entities/icon.html',
    link: function (scope, element, attrs, model) {
    }
  };
}]);
;datawire.directive('pager', ['$timeout', function ($timeout) {
    return {
        restrict: 'E',
        scope: {
            'response': '=',
            'load': '&load'
        },
        templateUrl: 'templates/directives/pager.html',
        link: function (scope, element, attrs, model) {
            scope.$watch('response', function(e) {
                scope.showPager = false;
                scope.pages = [];
                if (scope.response.pages <= 1) {
                    return;
                }
                var pages = [],
                    current = (scope.response.offset / scope.response.limit) + 1,
                    num = Math.ceil(scope.response.total / scope.response.limit),
                    range = 2,
                    low = current - range,
                    high = current + range;

                if (low < 1) {
                    low = 1;
                    high = Math.min((2*range)+1, num);
                }
                if (high > num) {
                    high = num;
                    low = Math.max(1, num - (2*range)+1);
                }

                for (var page = low; page <= high; page++) {
                    var offset = (page-1) * scope.response.limit,
                        url = scope.response.format.replace('LIMIT', scope.response.limit).replace('OFFSET', offset);
                    pages.push({
                        page: page,
                        current: page==current,
                        url: url
                    });
                }
                scope.showPager = true;
                scope.pages = pages;
            });
        }
    };
}]);
;datawire.directive('watchlistFrame', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'list': '=',
      'selected': '@'
    },
    templateUrl: 'templates/watchlists/frame.html',
    link: function (scope, element, attrs, model) {
      $http.get('/api/1/lists').then(function(res) {
        scope.lists = res.data;
      })
    }
  };
}]);
;
datawire.controller('EntitiesIndexCtrl', ['$scope', '$location', '$http', '$routeParams', 'Validation', 'Flash',
  function($scope, $location, $http, $routeParams, Validation, Flash) {

  var apiUrl = '/api/1/lists/' + $routeParams.id;
  $scope.query = $location.search();
  $scope.list = {};
  $scope.entities = {};
  $scope.edit = null;
  $scope.newEntity = {'category': 'Person'};

  $http.get(apiUrl).then(function(res) {
    $scope.list = res.data;
  });

  $scope.setEdit = function(val, suggestCreate) {
    $scope.edit = val;
    if (suggestCreate) {
      $scope.newEntity = {
        'category': 'Person',
        'label': $scope.query.prefix
      };
    } else if (val) {
      setTimeout(function() {
        $('#edit-label-' + val).focus();
      }, 20);
    }
  };

  var handleResult = function(res) {
    $('#prefix-search').focus();
    angular.forEach(res.data.results, function(e) {
      var aliases = [];
      angular.forEach(e.selectors, function(s) {
        if (s !== e.label) {
          aliases.push(s);
        }
      });
      e.aliases = aliases.join(', ');
    });
    $scope.entities = res.data;
    if ($scope.entities.total == 0) {
      $scope.setEdit('new', true);
    }
  };

  var adaptEntity = function(entity) {
    entity.selectors = [];
    entity.list = $routeParams.id;
    entity.aliases = entity.aliases || '';
    angular.forEach(entity.aliases.split(','), function(s) {
      s = s.trim();
      if (s.length) entity.selectors.push(s);
    });
    return entity;
  };

  $scope.create = function(form) {
    var entity = adaptEntity($scope.newEntity);
    var res = $http.post('/api/1/entities', entity);
    res.success(function(data) {
      Flash.message("We track 'em, you whack 'em.", 'success');
      $scope.setEdit(null);
      $scope.entities.results.unshift(data);
      $scope.newEntity = {'category': 'Person'};
    });
    res.error(Validation.handle(form));
  };

  $scope.update = function(form, entity) {
    entity = adaptEntity(entity);
    var res = $http.post(entity.api_url, entity);
    res.success(function(data) {
      Flash.message("Your changes have been saved.", 'success');
      $scope.setEdit(null);
    });
    res.error(Validation.handle(form));
  };

  $scope.loadQuery = function() {
    $scope.setEdit(null);
    $scope.query['list'] = $routeParams.id;
    $http.get('/api/1/entities', {params: $scope.query}).then(handleResult);
  };

  $scope.loadUrl = function(url) {
    $http.get(url).then(handleResult);
  }

  $scope.filter = function() {
    delete $scope.query['list'];
    $location.search($scope.query);
  };

  $scope.delete = function(entity) {
    $http.delete(entity.api_url).then(function(res) {
      var idx = $scope.entities.results.indexOf(entity);
      $scope.entities.results.splice(idx, 1);
    });
  };

  $scope.$on('$routeUpdate', function(){
    $scope.loadQuery();
  });

  $scope.loadQuery();

}]);
;datawire.factory('Flash', ['$rootScope', '$timeout', function($rootScope, $timeout) {
  // Message flashing.
  var currentMessage = null;

  return {
    setMessage: function(message, type) {
      currentMessage = [message, type];
      $timeout(function() {
        currentMessage = null;
      }, 4000);
    },
    getMessage: function() {
      if (currentMessage) {
        return currentMessage[0];
      }
    },
    getType: function() {
      if (currentMessage) {
        return currentMessage[1];
      }
    }
  };
}]);
;datawire.factory('Session', ['$http', function($http) {
  var sessionDfd = null;

  var flush = function() {
    sessionDfd = null;
  };

  var logout = function(cb) {
    $http.post('/api/1/sessions/logout').then(function() {
      console.log('LOGOUTED!');
      flush();
      get(cb);
    });
  };

  var get = function(cb) {
    if (sessionDfd === null) {
      var data = {'_': new Date()}
      sessionDfd = $http.get('/api/1/sessions', {params: data});
    }
    sessionDfd.then(function(res) {
      cb(res.data);
    });
  };

  return {
    'get': get,
    'flush': flush,
    'logout': logout
  }
}]);
;
datawire.factory('Validation', ['Flash', function(Flash) {
  // handle server-side form validation errors.
  return {
    handle: function(form) {
      return function(res) {
        if (res.status == 400 || !form) {
          var errors = [];

          for (var field in res.errors) {
            form[field].$setValidity('value', false);
            form[field].$message = res.errors[field];
            errors.push(field);
          }
          if (angular.isDefined(form._errors)) {
            angular.forEach(form._errors, function(field) {
              if (errors.indexOf(field) == -1 && form[field]) {
                form[field].$setValidity('value', true);
              }
            });
          }
          form._errors = errors;
        } else {
          Flash.message(res.message || res.title || 'Server error', 'danger');
        }
      }
    }
  };
}]);
;datawire.controller('UsersProfileCtrl', ['$scope', '$location', '$modalInstance', '$http', 'Session',
  function($scope, $location, $modalInstance, $http, Session) {
  $scope.user = {};
  $scope.session = {};

  Session.get(function(session) {
    $scope.user = session.user;
    $scope.session = session;
  });

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };

  $scope.update = function(form) {
    var res = $http.post('/api/1/users/' + $scope.user.id, $scope.user);
    res.success(function(data) {
      $scope.user = data;
      $scope.session.user = data;
      $modalInstance.dismiss('ok');
    });
  };
}]);
;;datawire.controller('WatchlistsDeleteCtrl', ['$scope', '$location', '$http', '$modalInstance', 'list',
                                        'Flash', 'QueryContext',
  function($scope, $location, $http, $modalInstance, list, Flash, QueryContext) {
  $scope.list = list;

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };

  $scope.delete = function() {
    var res = $http.delete($scope.list.api_url);
    res.then(function(data) {
        QueryContext.reset();
        $location.path('/');
        $modalInstance.dismiss('ok');
    });
  };

}]);
;datawire.controller('WatchlistsEditCtrl', ['$scope', '$location', '$http', '$routeParams', '$modal',
                                          'Flash', 'Validation', 'QueryContext',
  function($scope, $location, $http, $routeParams, $modal, Flash, Validation, QueryContext) {

  var apiUrl = '/api/1/lists/' + $routeParams.id;
  $scope.list = {};
  $scope.users = {};

  $http.get(apiUrl).then(function(res) {
    $scope.list = res.data;
  })

  $http.get('/api/1/users').then(function(res) {
    $scope.users = res.data;
  })

  $scope.canSave = function() {
    return $scope.list.can_write;
  };

  $scope.hasUser = function(id) {
    var users = $scope.list.users || [];
    return users.indexOf(id) != -1;
  };

  $scope.toggleUser = function(id) {
    var idx = $scope.list.users.indexOf(id);
    if (idx != -1) {
      $scope.list.users.splice(idx, 1);
    } else {
      $scope.list.users.push(id);
    }
  };

  $scope.delete = function() {
    var d = $modal.open({
        templateUrl: 'templates/watchlists/delete.html',
        controller: 'WatchlistsDeleteCtrl',
        resolve: {
            list: function () { return $scope.list; }
        }
    });
  }

  $scope.save = function(form) {
    var res = $http.post(apiUrl, $scope.list);
    res.success(function(data) {
      QueryContext.reset();
      Flash.message('Your changes have been saved.', 'success');
    });
    res.error(Validation.handle(form));
  };

}]);
;datawire.controller('WatchlistsIndexCtrl', ['$scope', function($scope) {

}]);
;datawire.controller('WatchlistsNewCtrl', ['$scope', '$location', '$http', '$routeParams', 'Validation',
  function($scope, $location, $http, $routeParams, Validation, QueryContext) {
  $scope.list = {'public': false, 'new': true};

  $scope.canCreate = function() {
    return $scope.session.logged_in;
  };

  $scope.create = function(form) {
      var res = $http.post('/api/1/lists', $scope.list);
      res.success(function(data) {
        $location.path('/lists/' + data.id + '/entities');
      });
      res.error(Validation.handle(form));
  };

}]);
