'use strict';

/* Controllers */

var mod = angular.module('guampa.controllers', []);

mod.controller(
    'MenuCtrl',
    ['$scope','$location',
function ($scope, $location) {
	$scope.menuList = [
	   {id:0, url:'#/start', text:'START', style:""},
	   {id:1, url:'#/browse', text:'BROWSE', style:""},
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

function translateCtrl($scope, $routeParams, $http, DocumentAndTranslation) {
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
}
