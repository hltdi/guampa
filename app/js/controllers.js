'use strict';

/* Controllers */

function MenuCtrl($scope, $location) {
	$scope.menuList = [
	   {id:0, url:'#/search', text:"Inicio", style:""},
	   {id:1, url:'#/upload', text:"Subir un Documento", style:""},
	   {id:2, url:'#/catalog', text:"Catalogo", style:""},
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
