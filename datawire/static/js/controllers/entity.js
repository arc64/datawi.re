
function EntityCtrl($scope, $rootScope, $routeParams, $http, identity) {
    $scope.showCreateForm = false;
    $scope.createForm = {'category': 'orgs'};

    $scope.selectedClass = function(entity) {
        return $scope.selected(entity.id) ? 'selected' : 'unselected';
    };

    $scope.selectedCategory = function(key) {
        return $scope.createForm.category == key ? 'active' : 'inactive';
    };

    $scope.newFormLinkIcon = function() {
        return $scope.showCreateForm ? 'icon-minus-sign' : 'icon-plus-sign';
    };

    $rootScope.$on('createEntity', function(e, text) {
        $scope.createForm.text = text;
        $scope.showCreateForm = true;
        $scope.$apply();
    });

    $scope.create = function() {
        $http.post('/api/1/entities', $scope.createForm).success(function(data) {
            $scope.entities[$scope.createForm.category].push(data);
        });
        $scope.createForm.text = null;
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
