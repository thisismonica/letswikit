/**
 * Created by Suparn Gupta on 10/2/15.
 */
angular.module("portal")
    .controller("Top", function ($scope, $rootScope, $state) {
        var q = {
            "query": {
                "match_all": {}
            }
        };
        var es = new elasticsearch.Client({
            host: "localhost:9200"
        });
        es.search({
            index: 'test3',
            body: q
        }).then(function (resp) {

            var hits = resp.hits.hits;
            $scope.topics = hits;
            console.log(hits);
            $scope.$apply();
        }, function (err) {
            console.trace(err.message);
        });


        $scope.goToTopic2 = function (topic) {
            console.log("I am inside this topic");
            $rootScope.currentTopic = topic;
            $state.go("article");
        };

        $scope.goToTopic = function (topic) {
            console.log("I am inside this topic");
            $rootScope.currentTopic = topic;
            $state.go($state.current, {}, {reload: true})
        }
    });