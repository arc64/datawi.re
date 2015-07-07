from flask.ext.assets import Bundle

from datawire.core import assets

deps_assets = Bundle(
    'vendor/angular/angular.js',
    'vendor/ng-debounce/angular-debounce.js',
    'vendor/angular-route/angular-route.js',
    'vendor/angular-animate/angular-animate.js',
    'vendor/angular-loading-bar/build/loading-bar.js',
    'vendor/angular-truncate/src/truncate.js',
    'vendor/angular-bootstrap/ui-bootstrap-tpls.js',
    'vendor/nginfinitescroll/build/ng-infinite-scroll.js',
    filters='uglifyjs',
    output='assets/deps.js'
)

app_assets = Bundle(
    'js/util.js',
    'js/app.js',
    'js/services.js',
    'js/lists.js',
    'js/entities.js',
    'js/directives.js',
    'js/ctrl.js',
    filters='uglifyjs',
    output='assets/app.js'
)

css_assets = Bundle(
    'style/style.less',
    'vendor/angular-loading-bar/build/loading-bar.css',
    'style/animations.css',
    filters='less',
    output='assets/style.css'
)

assets.register('deps', deps_assets)
assets.register('app', app_assets)
assets.register('css', css_assets)
