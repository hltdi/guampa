function translateCtrl($scope) {
    $scope.editedItem = null;
    $scope.sentences = [{ content: "My cat is brown" },
                        { content: "My dog is black" },
                        { content: "Lorem ipsum dolor sit amet, consectetur adipisicing elit." }];

    $scope.editTranslation = function(sentence) {
        $scope.editedItem = sentence;
    };                    

    $scope.finishTranslation = function(sentence) {
        $scope.editedItem = null;
    };
};

function commentsCtrl($scope, $modal) {
    $scope.comments = ["comment1", "comment2", "comment3"];

    $scope.openComments = function() {
        var modalInstance = $modal.open({
            templateUrl: 'comments.html',
            controller: CommentsInstanceController,
            resolve: {
                comments: function() {
                    return $scope.comments;
                }
            }
        });
    };
};

function CommentsInstanceController($scope, $modalInstance, comments) {
    $scope.comments = comments;
    $scope.close = function() {
        $modalInstance.close();
    }
};

angular.module('translateApp', ['ui.bootstrap']);