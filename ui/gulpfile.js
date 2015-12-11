'use strict';

var path = require('path');
var gulp = require('gulp');
var less = require('gulp-less');
var del = require('del');
var minifycss = require('gulp-minify-css');
var LessPluginCleanCss = require("less-plugin-clean-css");
var cleanCSS = new LessPluginCleanCss({advanced: true});
var concat = require("gulp-concat");
var ngAnnotate = require("gulp-ng-annotate");
var uglify = require('gulp-uglify');
var watch = require('gulp-watch');
var angularTemplates = require("gulp-angular-templates");
var plumber = require("gulp-plumber");

var errorHandler = function (error) {
    console.error(error.toString());
    this.emit('end');
};

//scripts
var scripts = ['./static/src/js/app.js', './static/src/js/controllers/*.js', './static/src/js/services/*.js', './static/src/js/directives/*.js'];
gulp.task('scripts', function () {
    return gulp.src(scripts)
        .pipe(plumber({errorHandler: errorHandler}))
        .pipe(concat('portal.js'))
        .pipe(ngAnnotate())
        .pipe(gulp.dest('./static/dist/js'))
});

//less
var css = ['./static/src/less/*.less'];
gulp.task('less', function () {
    return gulp.src(css)
        .pipe(plumber({errorHandler: errorHandler}))
        .pipe(less())
        .pipe(concat('portal.min.css'))
        .pipe(minifycss())
        .pipe(gulp.dest('./static/dist/css'));
});

//vendor JS
var vendorJS = ['static/vendor/plugins/jquery/jquery-1.11.1.min.js', 'static/vendor/plugins/boostrapv3/js/bootstrap.min.js',
    'static/vendor/plugins/angular/angular.js', 'static/vendor/plugins/angular-bootstrap/ui-bootstrap.min.js', 'static/vendor/plugins/angular-bootstrap/ui-bootstrap-tpls.min.js',
    'static/vendor/plugins/elasticsearch/elasticsearch.min.js',
    'static/vendor/plugins/angular-ui-router/angular-ui-router.min.js',
    'static/vendor/plugins/angular-sanitize/angular-sanitize.min.js', 'static/vendor/plugins/angular-cookies/angular-cookies.min.js',
    'static/vendor/plugins/lodash/lodash.min.js'];

gulp.task('vendorJS', function () {
    return gulp.src(vendorJS)
        .pipe(plumber({errorHandler: errorHandler}))
        .pipe(concat('vendor.min.js'))
        .pipe(gulp.dest('./static/dist/js/'))
});

//vendor CSS
var vendorCSS = ['static/vendor/plugins/boostrapv3/css/bootstrap.min.css', 'static/vendor/plugins/angular-bootstrap/ui-bootstrap-csp.css',
    'static/vendor/plugins/font-awesome/css/font-awesome.css', 'static/vendor/css/style.css'];

gulp.task('vendorCSS', function () {
    return gulp.src(vendorCSS)
        .pipe(plumber({errorHandler: errorHandler}))
        .pipe(concat('vendor.min.css'))
        .pipe(minifycss('vendor.min.css'))
        .pipe(gulp.dest('./static/dist/css'));
});

//templates
var templates = ['./static/src/templates/**/*.html'];
gulp.task('templates', function () {
    return gulp.src(templates)
        .pipe(plumber({errorHandler: errorHandler}))
        .pipe(angularTemplates({basePath: '/static/dist/templates/', module: 'portal'}))
        .pipe(concat('templates.min.js'))
        .pipe(gulp.dest('./static/dist/js/'));
});


//fonts
var fonts = ['./static/vendor/fonts/**/*', './static/vendor/plugins/font-awesome/fonts/*'];
gulp.task('fonts', function () {
    return gulp.src(fonts)
        .pipe(plumber({errorHandler: errorHandler}))
        .pipe(gulp.dest('./static/dist/fonts'));
});

//images
var images = ['./static/vendor/img/**/*'];
gulp.task('images', function () {
    return gulp.src(images)
        .pipe(plumber({errorHandler: errorHandler}))
        .pipe(gulp.dest('./static/dist/img'));
});

//clean
gulp.task('clean', function (cb) {
    del(['./static/dist'], cb);
});


gulp.task('build', ['scripts', 'less', 'vendorJS', 'vendorCSS', 'fonts', 'images', 'templates']);

gulp.task('dist', ['clean'], function () {
    gulp.start('build');
});

gulp.task('watch', function () {
    watch(scripts, function () {
        gulp.start('scripts');
    });

    watch(css, function () {
        gulp.start('css');
    });

    watch(templates, function () {
        gulp.start('templates');
    });
});