
function EntityCtrl($scope, $routeParams, $http, identity) {
    $scope.showCreateForm = false;
    $scope.create_form = {'category': 'orgs'};

    $scope.selectedClass = function(entity) {
        return $scope.selected(entity.id) ? 'selected' : 'unselected';
    };

    $scope.selectedCategory = function(key) {
        return $scope.create_form.category == key ? 'active' : 'inactive';
    };

    $scope.newFormLinkIcon = function() {
        return $scope.showCreateForm ? 'icon-minus-sign' : 'icon-plus-sign';
    };

    $scope.$watch('_createEntity', function(newValue, oldValue) {
        $scope.create_form.text = newValue;
        $scope.showCreateForm = true;
    });

    $scope.create = function() {
        $http.post('/api/1/entities', $scope.create_form).success(function(data) {
            $scope.entities[$scope.create_form.category].push(data);
        });
        $scope.create_form.text = null;
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
