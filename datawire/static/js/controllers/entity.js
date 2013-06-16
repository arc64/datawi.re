
function EntityCtrl($scope, $routeParams, $http, identity) {
    $scope._new = {};



    $scope.selectedClass = function(entity) {
        return $scope.selected(entity.id) ? 'selected' : 'unselected';
    };

    $scope.create = function(category) {
        data = {category: category, text: $scope._new[category]};
        $scope._new[category] = '';
        $http.post('/api/1/entities', data).success(function(data) {
            $scope.entities[category].push(data);
        });
    };

    $scope.remove = function(category, id) {
        $http({method: 'delete', url: '/api/1/entities/' + id}).error(function(data, status) {
            if (status===410) {
                var entities = [];
                angular.forEach($scope.entities[category], function(entity) {
                    if (entity.id!==id) entities.push(entity);
                });
                $scope.entities[category] = entities;
            }
        });
    };
}
