
datawire.factory('feed', function($http, identity, services, facets) {
    var currentData = null,
        entities = [];
    var notify = { updateFrames: null, updateEntities: null };

    function feedQuery() {
        // mostly a workaround for broken query builder in $http, 
        // fixed in angular 1.1.5.
        var query = ['limit=15'];
        angular.forEach(entities, function(e) {
            query.push('entity=' + encodeURIComponent(e));
        });
        return '?' + query.join('&');
    }

    function loadFrames(url, callback) {
        $http.get(url).success(function(data) {
            angular.forEach(data.results, function(frame, i) {
                services.getFrame(frame);
            });
            callback(data);
        });
    }

    function loadFacetEntities(facet_name) {
        identity.session(function(ident) {
            $http.get('/api/1/users/' + ident.user.id + '/entities?facet='+facet_name)
            .success(function(data) {
                
                notify.updateEntities(facet_name, data.results);
            });
        });
    }

    function update() {
        facets.getAll(function(data) {
            angular.forEach(data.results, function(facet) {
                loadFacetEntities(facet.key);
            });
        });

        identity.session(function(ident) {
            loadFrames('/api/1/users/' + ident.user.id + '/feed' + feedQuery(), function(data) {
                currentData = data;
                notify.updateFrames(data);
            });
        });
    }

    function loadMore() {
        loadFrames(currentData.next, function(data) {
            currentData.results = currentData.results.concat(data.results);
            currentData.next = data.next;
            notify.updateFrames(currentData);
        });
    }

    function hasMore() {
        return currentData && !!currentData.next;
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
        loadMore: loadMore,
        hasMore: hasMore,
        entitySelected: entitySelected,
        toggleEntity: toggleEntity
    };
});
