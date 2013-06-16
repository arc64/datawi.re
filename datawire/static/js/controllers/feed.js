
function FeedCtrl($scope, $routeParams, $http, identity, services, categories) {
    $scope.entities = {};
    $scope.frames = [];
    $scope.count = 0;
    $scope.entityFilters = [];

    var currentData = null;

    function queryFilter() {
        var query = [];
        angular.forEach($scope.entityFilters, function(e) {
            query.push('entity=' + encodeURIComponent(e));
        });
        return query;
    }

    $scope.selected = function(id) {
        return $scope.entityFilters.indexOf(id) != -1;
    };

    $scope.toggle = function(id) {
        if ($scope.selected(id)) {
            $scope.entityFilters = _.without($scope.entityFilters, id);
        } else {
            $scope.entityFilters.push(id);
        }
        $scope.update();
    };

    function loadFrames(url, callback) {
        $http.get(url).success(function(data) {
            angular.forEach(data.results, function(frame, i) {
                services.getFrame(frame);
            });
            callback(data);
        });
    }

    function loadCategoryEntities(category) {
        identity.session(function(ident) {
            var query = ['category='+category, 'limit=15'];
            query = query.concat(queryFilter());
            $http.get('/api/1/users/' + ident.user.id + '/entities?' + query.join('&'))
            .success(function(data) {
                $scope.entities[category] = data.results;
            });
        });
    }

    $scope.update = function() {
        categories.getAll(function(data) {
            $scope.categories = data.results;
            angular.forEach(data.results, function(category) {
                loadCategoryEntities(category.key);
            });
        });

        identity.session(function(ident) {
            var query = ['limit=15'];
            query = query.concat(queryFilter());
            loadFrames('/api/1/users/' + ident.user.id + '/feed?' + query.join('&'), function(data) {
                currentData = data;
                $scope.frames = data.results;
                $scope.count = data.count;
            });
        });
    };

    $scope.loadMore = function() {
        loadFrames(currentData.next, function(data) {
            currentData.results = currentData.results.concat(data.results);
            currentData.next = data.next;
            $scope.frames = currentData.results;
            $scope.count = data.count;
        });
    };

    $scope.hasMore = function() {
        return currentData && !!currentData.next;
    };

    $scope.update();
};
