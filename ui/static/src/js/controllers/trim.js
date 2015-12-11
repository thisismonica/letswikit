/**
 * Created by IronMan on 10/2/15.
 */

angular.module('portal').filter('trim', function () {
    return function (input, length) {
        length = length ? length : 20;
        return _.trunc(input, length);
    }
});

angular.module('portal').filter('escapeHTML', function () {
    return function (input) {
        return _.escape(input).replace(/\n$/, '<br/>&nbsp;').replace(/\n/g, '<br/>');
    };
});