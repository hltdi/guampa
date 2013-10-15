function translateCtrl($scope) {
    $scope.editedItem = null;
    $scope.sentences = [{ content: "My cat is brown", editing: false },
                        { content: "My dog is black", editing: false },
                        { content: "Lorem ipsum dolor sit amet, consectetur adipisicing elit.", editing: false}];

    $scope.editTranslation = function(sentence) {
        $scope.editedItem = sentence;
    };                    

    $scope.finishTranslation = function(sentence) {
        $scope.editedItem = null;
    };
}