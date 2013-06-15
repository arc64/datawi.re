
datawire.factory('identity', function($http) {
    var dfd = $http.get('/api/1/sessions');
    return {
        session: dfd.success,
        checkSession: function(callback) {
            dfd.success(function(data) {
                if (!data.logged_in) {
                    callback(data);
                }
            });
        }
    };
});
