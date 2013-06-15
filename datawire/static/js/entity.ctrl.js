
function EntityCtrl($scope, $routeParams, $http, identity, feed, facets) {
    $scope._new = {};
    $scope.entities = {};

    facets.getAll(function(facets) {
        $scope.facets = facets.results;
    });

    $scope.isSelected = function(entity) {
        return feed.entitySelected(entity.id) ? 'selected' : 'unselected';
    };

    feed.notify.updateEntities = function(facet_name, data) { 
        $scope.entities[facet_name] = data;
    };

    $scope.toggle = feed.toggleEntity;

    $scope.create = function(facet) {
        data = {facet: facet, text: $scope._new[facet]};
        $scope._new[facet] = '';
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
