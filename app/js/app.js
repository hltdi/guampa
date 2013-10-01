'use strict';

/* App Module */

angular.module('guampa', []).
config(['$locationProvider','$routeProvider',
    function($locationProvider, $routeProvider) {
      $routeProvider.
        when('/inicio', {templateUrl: 'partials/inicio.html'}).
        when('/ohai', {templateUrl: 'partials/ohai.html'}).
        otherwise({redirectTo: '/inicio'});

      // XXX: when do we need this? ...
      // $locationProvider.html5Mode(true);
}]);
