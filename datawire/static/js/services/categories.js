datawire.factory('categories', function($q, $http) {
    return {
        getAll: $http.get('/api/1/categories').success
    };
});