datawire.directive('entityIcon', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'category': '='
    },
    templateUrl: 'templates/entities/icon.html',
    link: function (scope, element, attrs, model) {
    }
  };
}]);
