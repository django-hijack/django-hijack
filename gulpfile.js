var gulp = require('gulp');
var rename = require('gulp-rename')
var postcss = require('gulp-postcss');
var sass = require('gulp-sass')(require('sass'));

var autoprefixer = require('autoprefixer');
var cssnano = require('cssnano');

var buildLib = process.env.BUILD_LIB || '.';

gulp.task('css', function () {
    var processors = [
        autoprefixer,
        cssnano
    ];
    return gulp.src('./hijack/static/hijack/hijack.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(postcss(processors))
        .pipe(rename('hijack.min.css'))
        .pipe(gulp.dest('./hijack/static/hijack', { cwd: buildLib }));
});


gulp.task('css:watch', () => {
  gulp.watch('./hijack/static/hijack/hijack.scss', { ignoreInitial: false }, gulp.series('css'));
})
