
function ProfileCtrl($scope, $routeParams, $http, $location) {
    $http.get('/api/1/profile').success(function(data) {
        $scope.profile = data;
    });

    $scope.save = function() {
        var dfd = $http.post('/api/1/profile', $scope.profile);
        dfd.success(function(data) {
            $scope.profile = data;
            $scope.flash('success', 'Your profile has been updated.');
            $location.path('/');
        });
        dfd.error(function(data) {
            $scope.flash('error', 'There was an error saving your profile.');
        });
    };
}
