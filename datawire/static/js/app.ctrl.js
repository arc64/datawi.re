
function AppCtrl($scope, $window, $routeParams, $location, identity) {
    identity.session(function(data) {
        $scope.session = data;
    });

    $scope.$on("$routeChangeStart", function (event, next, current) {
        if (next && next.$$route.accessPolicy==='user') {
            identity.checkSession(function(data) {
                $location.path('/');
                $scope.flash('error', 'Sorry, you need to be logged in to view this page.');
            });
        }
    });

    $scope.flash = function(type, message) {
        $scope.currentFlash = {
            visible: true,
            type: type,
            message: message
        };
    };
}
