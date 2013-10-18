'use strict';

/* App Module */

var app = angular.module('guampa',
                         ['allDocumentsService',
                          'allTagsService',
                          'documentsForTagService',
                          'documentAndTranslationService',
                          'sentenceHistoryService',
                          'guampa.controllers',
                          'pascalprecht.translate']);

app.config(['$locationProvider','$routeProvider',
    function($locationProvider, $routeProvider) {
      $routeProvider.
        when('/start', {templateUrl: 'partials/start.html'}).
        when('/edit/:docid', {templateUrl: 'partials/edit.html',
                              controller: 'translateCtrl'}).
        when('/browse', {templateUrl: 'partials/browse.html',
                         controller: 'BrowseCtrl'}).
        when('/browse/*tagname', {templateUrl: 'partials/browse.html',
                                  controller: 'BrowseCtrl'}).
        when('/sentence/:sentenceid', {templateUrl: 'partials/sentence.html',
                                      }).
        otherwise({redirectTo: '/start'});
}]);

// Load up all of our translations.
app.config(['$translateProvider', function ($translateProvider) {
  for (var code in codes_to_translations) {
    if (codes_to_translations.hasOwnProperty(code)) {
      var translation = codes_to_translations[code];
      $translateProvider.translations(code, translation);
    }
  }
  $translateProvider.fallbackLanguage('en');
  $translateProvider.preferredLanguage('en');
}]);

