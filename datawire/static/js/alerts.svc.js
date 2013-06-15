
datawire.factory('alertService', function() {
    var alert = {
        visible: false,
        type: null,
        message: null
    };

    return {
        flash: function(type, message) {
            alert.visible = true;
            alert.type = type;
            alert.message = message;
        },
        hide: function() {
            alert.visible = false;
        },
        get: function() {
            return alert;
        }
    };
});
