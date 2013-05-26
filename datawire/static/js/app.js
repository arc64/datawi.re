
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

  $routeProvider.when('/', {
    templateUrl: '/static/partials/home.html',
    controller: HomeCtrl
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });

  $locationProvider.html5Mode(true);
});

datawire.directive('external', function ($window) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind('click', function() {
                $window.location.href = attrs.external;
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

datawire.factory('services', function($q, $http) {
    var serviceDfds = {};

    function getService(name, callback) {
        if(!serviceDfds[name]) {
            serviceDfds[name] = $http.get('/api/1/services/' + name);
        }
        serviceDfds[name].success(callback);
        return serviceDfds[name];
    }

    function getFrame(ref) {
        $http.get(ref.store_uri).success(function(frame) {
            getService(frame.service, function(service) {
                ref.event = _.find(service.events, function(e) {
                    return e.key == frame.event;
                });
                if(ref.event.tmpl===undefined) {
                    ref.event.tmpl = Handlebars.compile(ref.event.template);
                }
                ref.service = service;
                ref.data = frame.data;
                ref.message = ref.event.tmpl(frame.data);
            });
        });
    }

    return {
        getService: getService,
        getFrame: getFrame
    };
});

function FeedCtrl($scope, $routeParams, $http, services) {
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
        angular.forEach($scope.frames, function(frame, i) {
            services.getFrame(frame);
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
