var gulp = require("gulp");
var cssnano = require("gulp-cssnano"); // 压缩css文件的包
var rename = require("gulp-rename"); // 重命名的包
var uglify = require("gulp-uglify"); // js缩小文件的包
var concat = require("gulp-concat"); // 合并文件的包
var cache = require("gulp-cache"); // 缓存文件图片的包
var imagemin = require("gulp-imagemin"); // 合并图片的包
var bs = require("browser-sync").create(); //刷新浏览器
var sass = require("gulp-sass");  // 制作css工具
var util = require("gulp-util"); // 插件中有个log方法可以打印出js出错信息
var sourcemaps = require("gulp-sourcemaps");

var path = {
    "html": './templates/**/',
    "css": './src/css/**/',
    "js": './src/js/',
    "images": './src/images/',
    "dist_css": './dist/css/',
    "dist_js": './dist/js/',
    "dist_images": './dist/images/'
};

gulp.task("html", function (done) {
   gulp.src(path.html + "*.html")
       .pipe(bs.stream());
   done();
});

gulp.task("css", function (done) {
   gulp.src(path.css + "*.scss")
       .pipe(sass().on("error", sass.logError))
       .pipe(cssnano())
       .pipe(rename({suffix: '.min'}))
       .pipe(gulp.dest(path.dist_css))
       .pipe(bs.stream());
   done();
});

gulp.task("js", function (done) {
    gulp.src(path.js + "*.js")
        .pipe(sourcemaps.init())
        .pipe(uglify().on("error", util.log))
        .pipe(rename({suffix: '.min'}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.dist_js))
        .pipe(bs.stream());
    done();
});

gulp.task("images", function (done) {
    gulp.src(path.images + "*.*")
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.dist_images))
        .pipe(bs.stream());
    done();
});

gulp.task("bs", function () {
   bs.init({
       server:{
           baseDir: './'
       }
   });
});

gulp.task("watch", function (done) {
   gulp.watch(path.html + '*.html', gulp.series('html'));
   gulp.watch(path.css + '*.scss', gulp.series('css'));
   gulp.watch(path.js + '*.js', gulp.series('js'));
   gulp.watch(path.images + '*.*', gulp.series('images'));
});

// gulp.task("default", gulp.parallel("watch","bs"));
gulp.task("default", gulp.parallel("watch"));