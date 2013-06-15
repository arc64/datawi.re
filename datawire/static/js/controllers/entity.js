
function EntityCtrl($scope, $routeParams, $http, identity) {
    $scope._new = {};



    $scope.selectedClass = function(entity) {
        return $scope.selected(entity.id) ? 'selected' : 'unselected';
    };

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
                    if (entity.id!==id) entities.push(entity);
                });
                $scope.entities[facet] = entities;
            }
        });
    };
}
