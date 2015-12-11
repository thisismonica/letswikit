/* ============================================================
 * File: app.js
 * Configure global module dependencies. Page specific modules
 * will be loaded on demand using ocLazyLoad
 * ============================================================ */

'use strict';

var portal = angular.module('portal', [
    'ui.router'
    , 'ngSanitize',
    'ui.bootstrap'
]);

portal.provider('template', function () {
    var fetchViewWithName = function (name) {
        return '/static/dist/templates/' + name + '.html';
    };
    var fetchPartialWithName = function (name) {
        return '/static/dist/templates/blocks/' + name + '.html';
    };

    return {
        fetchViewWithName: fetchViewWithName,
        fetchPartialWithName: fetchPartialWithName,
        $get: function () {
            return {
                fetchViewWithName: fetchViewWithName,
                fetchPartialWithName: fetchPartialWithName
            }
        }
    }
});

portal
    .config(function ($stateProvider, $urlRouterProvider, templateProvider) {
        $urlRouterProvider
            .otherwise('/');

        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: templateProvider.fetchViewWithName('home')
            })
            .state('recent', {
                url: "/recent",
                templateUrl: templateProvider.fetchViewWithName('recent'),
                controller: 'Recent'
            })
            .state('article', {
                url: "/article",
                templateUrl: templateProvider.fetchViewWithName('article'),
                controller: 'Article'
            });

    });

portal.controller('AppCtrl', function ($scope) {
    $scope.app = {name: "LetsWikiT"};
});