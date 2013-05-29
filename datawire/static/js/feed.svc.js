
datawire.factory('feed', function($http, identity, services) {
    var entities = [];
    var notify = { update: null };

    function feedQuery() {
        // mostly a workaround for broken query builder in $http, 
        // fixed in angular 1.1.5.
        var query = [];
        angular.forEach(entities, function(e) {
            query.push('entity=' + encodeURIComponent(e));
        });
        return '?' + query.join('&');
    }

    function update() {
        identity.session(function(ident) {
            $http.get('/api/1/users/' + ident.user.id + '/feed' + feedQuery()).success(function(data) {
                angular.forEach(data.results, function(frame, i) {
                    services.getFrame(frame);
                });
                notify.update(data);
            });
        });
    }

    function entitySelected(id) {
        return entities.indexOf(id) != -1;
    }

    function toggleEntity(id, callback) {
        if (entitySelected(id)) {
            entities = _.without(entities, id);
        } else {
            entities.push(id);
        }
        update();
    }

    return {
        update: update,
        notify: notify,
        entitySelected: entitySelected,
        toggleEntity: toggleEntity
    };
});
