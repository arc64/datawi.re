
function FeedCtrl($scope, $routeParams, feed) {
    $scope.refresh = feed.update;
    $scope.loadMore = feed.loadMore;
    $scope.hasMore = feed.hasMore;

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
        $scope.count = data.count;
    };

    feed.update();

}
