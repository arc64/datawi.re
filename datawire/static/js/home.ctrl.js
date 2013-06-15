
function HomeCtrl($scope, $location, identity) {
    identity.session(function(data) {
        if (data.logged_in) {
            $location.path('/feed');
        }
    });
}
