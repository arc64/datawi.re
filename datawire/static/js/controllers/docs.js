
function DocsCtrl($scope, $routeParams) {
    $scope.template = '/static/partials/docs/' + $routeParams.page + '.html';

    $scope.active = function(path) {
        return $routeParams.page == path ? 'active' : '';
    };
}
