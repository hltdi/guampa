'use strict';

/* Controllers */

var mod = angular.module('guampa.controllers', []);

mod.controller(
    'MenuCtrl',
    ['$scope','$location', 'CurrentUser',
function ($scope, $location, CurrentUser) {
	$scope.menuList = [
	   {id:0, url:'#/browse', text:'BROWSE', style:""},
	   {id:1, url:'#/about', text:'ABOUT', style:""},
	   ];
	var i;
	for(i = 0; i < $scope.menuList.length; i++) {
		if($location.path() === $scope.menuList[i].url.substring(1)) {
			$scope.menuList[i].style = "active";
			break;
		}
	}
	$scope.changeActive = function(id) {
		var i;
		for(i = 0; i < $scope.menuList.length; i++) {
			$scope.menuList[i].style = "";
		}
		$scope.menuList[id].style = "active";
	}

    $scope.currentUser = null;
    $scope.refreshUser = function() {
        $scope.currentUser = CurrentUser.get();
    }
    $scope.refreshUser();

    $scope.$on('UserChanged', function(event, user) {
        $scope.currentUser = user;
    });
}]);

function BrowseCtrl($scope, $http, $routeParams,
                    AllDocuments, AllTags, DocumentsForTag) {
  $scope.$routeParams = $routeParams;
  $scope.query = $routeParams.query;

  $scope.allTags = AllTags.get();

  $scope.tagname = $routeParams.tagname;
  if ($scope.tagname) {
      $scope.tagDocuments = DocumentsForTag.get({tagname:$scope.tagname});
      $scope.notag = false;
  } else {
      $scope.tagDocuments = undefined;
      $scope.notag = true;
  }
}

mod.controller(
    'TranslateCtrl',
    ['$scope','$translate',
function ($scope, $translate) {
    $scope.changeLanguage = function (langKey) {
        $translate.uses(langKey);
    };
}]);

function translateCtrl($scope, $routeParams, $http, DocumentAndTranslation,
                       CurrentUser) {
    $scope.editedItem = null;

    var docid = $routeParams.docid;

    $scope.pairs = [];

    DocumentAndTranslation.get({docid:docid},
    // ooh child, these things take callbacks.
    function(thedocument) {
        for (var i=0; i < thedocument.sentences.length; i++) {
            var sent = {content: thedocument.sentences[i], editing: false}
            var trans = {content: thedocument.translations[i].text,
                         docid: thedocument.translations[i].docid,
                         sentenceid: thedocument.translations[i].sentenceid,
                         editing: false}
            var pair = [sent, trans];
            $scope.pairs.push(pair);
        }
    });

    $scope.startEditing = function(sentence) {
        sentence.editing = true;
        $scope.editedItem = sentence;
    }

    $scope.doneEditing = function(translation) {
        translation.editing = false;
        $scope.editedItem = null;

        $http.post('json/add_translation',
                   {text:translation.content,
                    sentenceid: translation.sentenceid,
                    documentid: translation.docid}).
            error(function(){
                alert("oh noes couldn't post translation for some reason");
            });
    }

    $scope.currentUser = null;
    $scope.refreshUser = function() {
        $scope.currentUser = CurrentUser.get();
    }
    $scope.refreshUser();

    $scope.$on('UserChanged', function(event, user) {
        $scope.currentUser = user;
    });
}

function sortByTs(array) {
    return array.sort(function(a, b) {
        var x = a['ts']; var y = b['ts'];
        return ((x < y) ? 1 : ((x > y) ? -1 : 0));
    });
}

function sentenceCtrl($scope, $routeParams, $http, SentenceHistory,
                      CurrentUser) {
    $scope.newcomment = {text:""};
    var sentenceid = $routeParams.sentenceid;

    $scope.refreshHistory = function() {
        SentenceHistory.get({sentenceid:sentenceid},
        function(sentencehistory) {
            $scope.text = sentencehistory.text;
            $scope.docid = sentencehistory.docid;
            $scope.items = sortByTs(sentencehistory.items);
        });
    }
    $scope.refreshHistory();

    $scope.sendComment = function(newcomment) {
        $http.post('json/add_comment',
                   {text: newcomment.text,
                    sentenceid: sentenceid,
                    documentid: $scope.docid}).
            success(function(){
                $scope.newcomment.text = "";
                $scope.refreshHistory();
            }).
            error(function(){
                alert("oh noes couldn't post comment for some reason");
            });
    }

    $scope.currentUser = null;
    $scope.refreshUser = function() {
        $scope.currentUser = CurrentUser.get();
    }
    $scope.refreshUser();
    $scope.$on('UserChanged', function(event, user) {
        $scope.currentUser = user;
    });
}

function LoginCtrl($scope, $route, $http, $rootScope, CurrentUser) {
    $scope.username = "";
    $scope.password = "";
    $scope.currentUser = null;

    $scope.doLogin = function(u,p) {
        $http.post('json/login',
                   {username: u, password: p}).
            success(function(data) {
                var user = CurrentUser.get();
                $scope.currentUser = user;
                $rootScope.$broadcast('UserChanged', user);
            }).
            error(function(){
                alert("oh noes couldn't log in for some reason");
            });
    }
    $scope.refreshUser = function() {
        var user = CurrentUser.get();
        $scope.currentUser = user;
        $rootScope.$broadcast('UserChanged', user);
    }
    $scope.refreshUser();

    $scope.$on('UserChanged', function(event, user) {
        $scope.currentUser = user;
    });
}

function LogoutCtrl($scope, $http, $rootScope, CurrentUser) {
    $scope.username = "";
    $scope.password = "";
    $scope.doLogout = function() {
        $http.get('json/logout').
            success(function() {
                $rootScope.$broadcast('UserChanged', null);
            }).
            error(function(){
                alert("oh noes couldn't log out for some reason");
            });
    }
    $scope.doLogout();

    $scope.$on('UserChanged', function(event, user) {
        $scope.currentUser = user;
    });
}
