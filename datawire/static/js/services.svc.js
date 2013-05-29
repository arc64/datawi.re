
datawire.factory('services', function($q, $http) {
    var serviceDfds = {};

    function getService(name, callback) {
        if(!serviceDfds[name]) {
            serviceDfds[name] = $http.get('/api/1/services/' + name);
        }
        serviceDfds[name].success(callback);
        return serviceDfds[name];
    }

    function getFrame(ref) {
        $http.get(ref.store_uri, {cache: true}).success(function(frame) {
            getService(frame.service, function(service) {
                ref.event = _.find(service.events, function(e) {
                    return e.key == frame.event;
                });
                if(ref.event.tmpl===undefined) {
                    ref.event.tmpl = Handlebars.compile(ref.event.template);
                }
                ref.service = service;
                ref.data = frame.data;
                ref.message = ref.event.tmpl(frame.data);
                ref.loaded = true;
            });
        });
    }

    return {
        getService: getService,
        getFrame: getFrame
    };
});