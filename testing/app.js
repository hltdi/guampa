function translateCtrl($scope) {
    $scope.editedItem = null;
    $scope.sentences = [{ content: "My cat is brown", editing: false },
                        { content: "My dog is black", editing: false },
                        { content: "Lorem ipsum dolor sit amet, consectetur adipisicing elit.", editing: false}];

    $scope.startEditing = function(sentence) {
        sentence.editing = true;
        $scope.editedItem = sentence;
    }

    $scope.doneEditing = function(sentence) {
        sentence.editing = false;
        $scope.editedItem = null;
    }
}