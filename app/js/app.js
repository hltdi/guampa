'use strict';

/* App Module */

angular.module('guampa', ['allDocumentsService']).
config(['$locationProvider','$routeProvider',
    function($locationProvider, $routeProvider) {
      $routeProvider.
        when('/start', {templateUrl: 'partials/start.html'}).
        when('/browse', {templateUrl: 'partials/browse.html',
                         controller: BrowseCtrl}).
        otherwise({redirectTo: '/start'});

      // XXX: when do we need this? ...
      // $locationProvider.html5Mode(true);
}]);
