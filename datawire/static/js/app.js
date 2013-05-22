
var datawire = angular.module('datawire', [], function($routeProvider, $locationProvider) {
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

datawire.run(function($rootScope) {
    $rootScope.visit = function(url) {
        $window.location.href = url;
    };

    $rootScope.tableObject = function(obj) {
        var table = {};
        angular.forEach(obj, function(v, k) {
            if (v && v.length) {
                table[k] = v;
            }
        });
        return table;
    };

    $rootScope.flash = function(type, message) {
        $rootScope.currentFlash = {
            visible: true,
            type: type,
            message: message
        };
    };
});

datawire.factory('identity', function($http) {
    var dfd = $http.get('/api/1/sessions');
    return {
        session: dfd.success
    };
});

function ProfileCntl($scope, $routeParams, $http) {
    $http.get('/api/1/profile').success(function(data) {
        $scope.profile = data;
    });

    $scope.save = function() {
        var dfd = $http.post('/api/1/profile', $scope.profile);
        dfd.success(function(data) {
            $scope.profile = data;
            $scope.flash('success', 'Your profile has been updated.');
        });
        dfd.error(function(data) {
            $scope.flash('error', 'There was an error saving your profile.');
        });
    };
}

function NavigationCntl($scope, $window, $routeParams, identity) {
    identity.session(function(data) {
        $scope.session = data;
    });
    $scope.visit = function(url) {
        $window.location.href = url;
    };
}

function FeedCntl($scope, $routeParams, $http) {
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
        console.log($scope.templates);
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