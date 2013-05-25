
var datawire = angular.module('datawire', [], function($routeProvider, $locationProvider) {
  $routeProvider.when('/profile', {
    templateUrl: '/static/partials/profile.html',
    controller: ProfileCtrl,
    accessPolicy: 'user'
  });

  $routeProvider.when('/feed', {
    templateUrl: '/static/partials/feed.html',
    controller: FeedCtrl,
    accessPolicy: 'user'
  });

  $routeProvider.when('/entities', {
    templateUrl: '/static/partials/watchlist.html',
    controller: EntityCtrl,
    accessPolicy: 'user'
  });

  $locationProvider.html5Mode(true);
});

datawire.directive('xlink', function ($window) {
    return {
        restrict: 'E',
        template: '<a href=""><span ng-transclude></span></a>',
        transclude: true,
        link: function(scope, element, attrs) {
            element.bind('click', function() {
                $window.location.href = attrs.href;
            });
        }
    };
});

Handlebars.registerHelper('entity', function(text) {
    text = Handlebars.Utils.escapeExpression(text);
    var result = '<strong>' + text + '</strong>';
    return new Handlebars.SafeString(result);
});

datawire.factory('identity', function($http) {
    var dfd = $http.get('/api/1/sessions');
    return {
        session: dfd.success,
        checkSession: function(callback) {
            dfd.success(function(data) {
                if (!data.logged_in) {
                    callback(data);
                }
            });
        }
    };
});

function FeedCtrl($scope, $routeParams, $http) {
    $scope.tableObject = function(obj) {
        var table = {};
        angular.forEach(obj, function(v, k) {
            if (v && v.length) {
                table[k] = v;
            }
        });
        return table;
    };

    $http.get('/api/1/frames?limit=20').success(function(data) {
        $scope.frames = data.results;
        $scope.services = data.services;
        $scope.templates = {};
        angular.forEach(data.services, function(service, key) {
            angular.forEach(service.events, function(event, i) {
                if (!$scope.templates[service.key]) {
                    $scope.templates[service.key] = {};
                }
                var tmpl = Handlebars.compile(event.template);
                $scope.templates[service.key][event.key] = tmpl;
            });
        });
        angular.forEach($scope.frames, function(frame, i) {
            $http.get(frame.api_uri).success(function(fd) {
                frame.data = fd.data;
                frame.renderedView = true;
                var tmpl = $scope.templates[fd.service][fd.event];
                frame.rendered = tmpl(fd.data);
            });
        });
    });
}

function EntityCtrl($scope, $routeParams, $http, identity) {
    $scope._new = {};
    $scope.entities = {};

    $http.get('/api/1/facets').success(function(data) {
        $scope.facets = data.results;
        angular.forEach(data.results, function(facet) {
            loadFacetEntities(facet.key);
        });
    });

    function loadFacetEntities(facet_name) {
        identity.session(function(ident) {
            $http.get('/api/1/users/' + ident.user.id + '/entities?facet='+facet_name)
            .success(function(data) {
                $scope.entities[facet_name] = data.results;
            });
        });
    }

    $scope.create = function(facet) {
        data = {facet: facet, text: $scope._new[facet]};
        $scope._new[facet] = '';
        console.log(data);
        $http.post('/api/1/entities', data).success(function(data) {
            $scope.entities[facet].push(data);
        });
    };

    $scope.remove = function(facet, id) {
        $http({method: 'delete', url: '/api/1/entities/' + id}).error(function(data, status) {
            if (status===410) {
                var entities = [];
                angular.forEach($scope.entities[facet], function(entity) {
                    console.log(entity);
                    if (entity.id!==id) entities.push(entity);
                });
                $scope.entities[facet] = entities;
            }
        });
    };
}
