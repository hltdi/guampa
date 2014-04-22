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
	   {id:2, url:'#/settings', text:'SETTINGS', style:""},
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

function translateCtrl($scope, $routeParams, $http, $rootScope,
                       DocumentAndTranslation, CurrentUser) {
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
            var dictionary = thedocument.dictionaries[i];
            var pair = [sent, trans, dictionary];
            $scope.pairs.push(pair);
        }
    });

    $scope.startEditing = function(sentence) {
        if ($scope.editedItem) {
            $scope.doneEditing($scope.editedItem);
            $scope.editedItem = null;
        }
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

    // dictionaries disabled by default for now
    $scope.setUseDictionary = function(tf) {
      $rootScope.useDictionary = tf;
    }

    
    // Make it easier to type letters with tildes; if you put an uptick in front
    // of a letter, replace it with the nasalized version of that letter.
    $scope.tildes= function(thing) {
      var s = thing.content;
      s = s.replace("^a", "ã");
      s = s.replace("^e", "ẽ");
      s = s.replace("^i", "ĩ");
      s = s.replace("^o", "õ");
      s = s.replace("^u", "ũ");
      s = s.replace("^y", "ỹ");
      s = s.replace("^g", "g̃");

      s = s.replace("^A", "Ã");
      s = s.replace("^E", "Ẽ");
      s = s.replace("^I", "Ĩ");
      s = s.replace("^O", "Õ");
      s = s.replace("^U", "Ũ");
      s = s.replace("^Y", "Ỹ");
      s = s.replace("^G", "G̃");

      // XXX: how do we maintain the current cursor position here?
      thing.content = s;
    }
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

// maybe decide to break out the admin-specific functions
function LoginCtrl($scope, $location, $http, $rootScope, $route, CurrentUser) {
    $scope.username = "";
    $scope.password = "";
    $scope.currentUser = null;
    $scope.loginError = false;

    $scope.doLogin = function(u,p) {
        $http.post('json/login',
                   {username: u, password: p}).
            success(function(data) {
                var user = CurrentUser.get();
                $scope.currentUser = user;
                $rootScope.$broadcast('UserChanged', user);
            }).
            error(function(){
                $scope.loginError = true;
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

    $scope.personaLogin = function() {
        navigator.id.request({
          siteName: 'Guampa'
        });
    };

    $scope.personaLogout = function() {
        navigator.id.logout();
        return false;
    };

    setupPersonaLogin($scope, $rootScope, $http, $route, $location);
}

function LogoutCtrl($scope, $http, $rootScope, CurrentUser) {
    $scope.username = "";
    $scope.password = "";
    $scope.doLogout = function() {
        navigator.id.logout();
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

// adapted from the flask persona example:
// https://github.com/mitsuhiko/flask/tree/master/examples/persona
function setupPersonaLogin($scope, $rootScope, $http, $route, $location) {
  navigator.id.watch({
    loggedInUser: $scope.currentUser,
    onlogin: function(assertion) {
      $.ajax({
        type: 'POST',
        url: '_auth/login',
        data: {assertion: assertion},
        success: function(res, status, xhr) {
          if (res == 'OK') {
            // TODO(alexr) no user found. Need to create one.
            $location.path("/createuser");
          } else {
            var user = res;
            $scope.currentUser = user;
            $rootScope.$broadcast('UserChanged', user);
            $location.path("/browse");
          }
          // need to call $scope.$apply() to make Angular pick up on changes
          $scope.$apply();
        },
        error: function(xhr, status, err) {
          navigator.id.logout();
          alert('Login failure: ' + err);
        }
      });

    },
    onlogout: function() {
      $.ajax({
        type: 'GET',
        url: 'json/logout',
        success: function(res, status, xhr) {
          $scope.currentUser = null;
          $rootScope.$broadcast('UserChanged', null);
        },
        error: function(xhr, status, err) {
          alert('Logout failure: ' + err);
        }
      });
    }
  });
}

function CreateUserCtrl($scope, $http, $location, $route, $rootScope,
                        CurrentEmail) {
    $scope.email = CurrentEmail.get();
    $scope.username = "";

    $scope.submit = function(username) {
        $http.post('json/create_persona_user',
                   {username:username}).
            success(function(user) {
                // alert("SUCECCS ACCOUNT CRETED");
                $scope.currentUser = user;
                $rootScope.$broadcast('UserChanged', user);
                $location.path("/browse");
                $route.reload();
                // XXX: should really log you in automatically here.
            }).
            error(function(){
                alert("Could not create account -- maybe the username is taken?");
            });
    }
}

function UploadCtrl($scope, $routeParams, SegmentedUpload) {
}

function ViewUploadCtrl($scope, $routeParams, $http, $location, $route, SegmentedUpload) {

    $scope.title = "";
    $scope.tags = "";

    var filename = $routeParams.filename;
    SegmentedUpload.get({filename:filename},
        function(segments) {
            $scope.segments = segments.segments;
        });

    $scope.merge = function(segmentid) {
        // actually do the merge.
        for(var i = 0; i < $scope.segments.length; i++) {
            var segment = $scope.segments[i];
            if (segment[0] == segmentid) {
                // once we've found it, take the text from the current one and
                // append it to the text of the previous one.
                var prevSegment = $scope.segments[i-1];
                prevSegment[1] = prevSegment[1] + " " + segment[1];
                $scope.segments.splice(i, 1);
                break;
            }
        }
    }

    // make the sentence editable.
    $scope.edit = function(segmentid) {
        var elt = document.getElementById("segment" + segmentid);
        elt.setAttribute("contenteditable", true);
        elt.focus();
    }

    function nextSegmentId() {
        var maxid = -1;
        for(var i = 0; i < $scope.segments.length; i++) {
            var segment = $scope.segments[i];
            if (segment[0] > maxid) {
                maxid = segment[0];
            }
        }
        return maxid + 1;
    }

    // Called when they hit the "save" button. Next, gotta find the line breaks
    // and create new segments in the model.
    $scope.modelsave = function(segmentid) {
        var elt = document.getElementById("segment" + segmentid);
        elt.setAttribute("contenteditable", false);

        for(var i = 0; i < $scope.segments.length; i++) {
            var segment = $scope.segments[i];
            if (segment[0] == segmentid) {
                var text = elt.innerText;
                var splits = text.split("\n"); // try splitting on newlines

                var newid = nextSegmentId();
                var newsegments = [];
                for (var j = 0; j < splits.length; j++) {
                    var segmentText = splits[j].trim();
                    if (segmentText) {
                        var newsegment = [newid + j, segmentText];
                        newsegments.push(newsegment);
                    }
                }
                // splice all of the segments in newsegments into place
                var args = [0, 1].concat(newsegments);
                Array.prototype.splice.apply($scope.segments, args);
                break;
            }
        }
    }

    $scope.saveToServer = function() {
        $http.post('json/save_document',
                   {segments:$scope.segments,
                    title:$scope.title,
                    tags:$scope.tags,
                    }).
            success(function(foo) {
                $location.path("/browse");
                $route.reload();
            }).
            error(function(){
                alert("oh noes couldn't upload document for some reason");
            });
    }
}
