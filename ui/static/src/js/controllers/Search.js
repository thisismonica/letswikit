/**
 * Created by Suparn Gupta on 10/2/15.
 */
angular.module("portal")
.controller('Search', function ($scope, $http, $state, $rootScope) {
        $scope.topics = [];
        $scope.loadingTopics = "Loading";
        $scope.noTopics = "No topics found";
        $scope.$watch("query.value", function (newValue) {
            if(!newValue){
                return;
            }
            console.log(newValue);
            $scope.queryES(newValue);
        });

        $scope.queryES = function (query) {
            var q = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "question.content": {
                                        "query": query + "*"
                                    }
                                }
                            },
                            {
                                "match": {
                                    "topic": {
                                        "query": query + "*",
                                        "boost": 3
                                    }
                                }
                            }
                        ]
                    }
                }
            };

            var es = new elasticsearch.Client({
                host: "localhost:9200"
            });
            es.search({
                index: 'test3',
                type: 'article',
                body: q
            }).then(function (resp) {
                var hits = resp.hits.hits;
                $scope.topics = hits;
                console.log(hits);
                $scope.$apply();
            }, function (err) {
                console.trace(err.message);
            });

            //$http.post("http://localhost:9200/test1/_search", q, {headers: {'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"}})
            //    .then(function (config) {
            //        var data = config.data;
            //        console.log(data.hits.hits);
            //        $scope.topics = data.hits.hits;
            //        console.log(data);
            //
            //    })
        };

        $scope.itemSelected = function (item, model) {
            console.log("modl", model);
            $rootScope.currentTopic = item;
            $state.go("article");
        };
    });