'use strict';

/* Services */

angular.module('allDocumentsService', ['ngResource']).
factory('AllDocuments',
    function($resource){
      return $resource('json/documents',
                       {},
                       {query: {method:'GET', isArray:true}});
    }
);

angular.module('allTagsService', ['ngResource']).
factory('AllTags',
    function($resource){
      return $resource('json/tags',
                       {},
                       {query: {method:'GET', isArray:true}});
    }
);


angular.module('documentsForTagService', ['ngResource']).
factory('DocumentsForTag',
    function($resource){
      return $resource('json/documents/:tagname',
                       {},
                       {query: {method:'GET', isArray:true}});
    }
);

angular.module('documentAndTranslationService', ['ngResource']).
factory('DocumentAndTranslation',
    function($resource){
      return $resource('json/document/:docid',
                       {},
                       {query: {method:'GET', isArray:true}});
    }
);

angular.module('sentenceHistoryService', ['ngResource']).
factory('SentenceHistory',
    function($resource){
      return $resource('json/sentencehistory/:sentenceid',
                       {},
                       {query: {method:'GET', isArray:true}});
    }
);

angular.module('currentUserService', ['ngResource']).
factory('CurrentUser',
    function($resource){
      return $resource('json/currentuser',
                       {},
                       {query: {method:'GET', isArray:true}});
    }
);
