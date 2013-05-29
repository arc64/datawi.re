
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

    function update(callback) {
        identity.session(function(ident) {
            $http.get('/api/1/users/' + ident.user.id + '/feed').success(function(data) {
                angular.forEach(data.results, function(frame, i) {
                    services.getFrame(frame);
                });
                callback(data);
            });
        });
    }

    return {
        update: update
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

    feed.update(function(data) {
        $scope.frames = data.results;
    });

}
