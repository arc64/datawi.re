datawire.factory('facets', function($q, $http) {
    return {
        getAll: $http.get('/api/1/facets').success
    };
});