
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

datawire.factory('feed', function($http, identity, services) {
    var entities = [13, 14];
    var notify = { update: null };

    function buildQuery() {
        // mostly a workaround for broken query builder in $http, 
        // fixed in angular 1.1.5.
        var query = [];
        angular.forEach(entities, function(e) {
            query.push('entity=' + encodeURIComponent(e));
        });
        return '?' + query.join('&');
    }

    function update() {
        identity.session(function(ident) {
            $http.get('/api/1/users/' + ident.user.id + '/feed' + buildQuery()).success(function(data) {
                angular.forEach(data.results, function(frame, i) {
                    services.getFrame(frame);
                });
                notify.update(data);
            });
        });
    }

    function entitySelected(id) {
        return entities.indexOf(id) != -1;
    }

    function toggleEntity(id, callback) {
        if (entitySelected(id)) {
            entities = _.without(entities, id);
        } else {
            entities.push(id);
        }
        update();
    }

    return {
        update: update,
        notify: notify,
        entitySelected: entitySelected,
        toggleEntity: toggleEntity
    };
});

function FeedCtrl($scope, $routeParams, feed) {
    $scope.tableObject = function(obj) {
        var table = {};
        angular.forEach(obj, function(v, k) {
            if (v && v.length) {
                table[k] = v;
            }
        });
        return table;
    };

    feed.notify.update = function(data) {
        $scope.frames = data.results;
    };

    feed.update();

}
