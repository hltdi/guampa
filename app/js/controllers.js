'use strict';

/* Controllers */

var mod = angular.module('guampa.controllers', []);

mod.controller(
    'MenuCtrl',
    ['$scope','$location',
function ($scope, $location) {
    // TODO(alexr): i18n for these interface strings.
	$scope.menuList = [
	   {id:0, url:'#/start', text:"Start", style:""},
	   {id:1, url:'#/browse', text:"Browse", style:""},
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

function BrowseCtrl($scope, $http, $routeParams, AllDocuments) {
  $scope.$routeParams = $routeParams;
  $scope.query = $routeParams.query;

  $scope.allDocuments = AllDocuments.get();
}

mod.controller(
    'TranslateCtrl',
    ['$scope','$translate',
function ($scope, $translate) {
    $scope.changeLanguage = function (langKey) {
        $translate.uses(langKey);
    };
}]);
