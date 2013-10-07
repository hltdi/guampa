'use strict';

/* Controllers */

function MenuCtrl($scope, $location) {
    // XXX: i18n for these interface strings.
	$scope.menuList = [
	   {id:0, url:'#/start', text:"Start", style:""},
	   {id:1, url:'#/browse', text:"Browse", style:""},
	   // {id:2, url:'#/catalog', text:"Catalogo", style:""},
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
}

function BrowseCtrl($scope, $http, $routeParams, AllDocuments) {
  $scope.$routeParams = $routeParams;
  $scope.query = $routeParams.query;

  $scope.allDocuments = AllDocuments.get();
}
