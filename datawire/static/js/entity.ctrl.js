
function EntityCtrl($scope, $routeParams, $http, identity, feed) {
    $scope._new = {};
    $scope.entities = {};

    $scope.isSelected = function(entity) {
        return feed.entitySelected(entity.id) ? 'selected' : 'unselected';
    };

    $scope.toggle = feed.toggleEntity;

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
