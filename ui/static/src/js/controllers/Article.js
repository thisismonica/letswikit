/**
 * Created by Suparn Gupta on 10/2/15.
 */
angular.module("portal")
.controller('Article', function ($scope, $rootScope) {
        console.log("Article", $rootScope.currentTopic);
        $scope.topic = $rootScope.currentTopic._source;
    });