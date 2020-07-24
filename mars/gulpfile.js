var gulp = require('gulp'),
    uglify = require('gulp-uglify'),
    rename = require('gulp-rename'),
    browserify = require('gulp-browserify'),
    concat = require('gulp-concat'),
    mocha = require('gulp-mocha'),
    shell = require('shelljs'),
    del = require('del'),
    jshint = require('gulp-jshint'),
    stylish = require('jshint-stylish'),
    semver = require('semver'),
    jsonfile = require('jsonfile'),
    inquirer = require("inquirer"),
    fs = require('fs');
var gulp        = require('gulp');
var deploy      = require('gulp-gh-pages');
var runSequence = require('run-sequence');
/**
 * Push build to gh-pages
 */
var gulp = require('gulp')
var runSeq = require('run-sequence')
var spawn = require('child_process').spawn;

gulp.task('serve', function() {
  spawn('node', ['index.js'], { stdio: 'inherit' });
});
gulp.task('heroku:production', function(){
  runSeq('clean', 'build', 'minify')
})
gulp.task('deploy', function () {
  return gulp.src("./src/visual/*")
    .pipe(deploy())
});
gulp.task('serveprod', function() {
  connect.server({
    root: ["/home/jaihonikhil/Desktop/THE-MARS-COLONIZATION-PROGRAM/"],
    port: process.env.PORT || 5000, // localhost:5000
    livereload: false
  });
});
gulp.task('clean', function(cb) {
    del('lib/**/*.*', cb);
});
gulp.task('build', function(callback) {
  runSequence('build-clean',
              ['build-scripts', 'build-styles'],
              'build-html',
              callback);
});
runSequence.options.ignoreUndefinedTasks = true;
gulp.task('task', function(cb) {
	runSequence('foo', null, 'bar'); // no longer errors on `null`
})
// configure build-clean, build-scripts, build-styles, build-html as you wish,
// but make sure they either return a stream or promise, or handle the callback
// Example:

gulp.task('build-clean', function() {
    // Return the Promise from del()
    return del([BUILD_DIRECTORY]);
//  ^^^^^^
//   This is the key here, to make sure asynchronous tasks are done!
});

gulp.task('heroku', ['wiredep','inject'], function () {
  return gulp.src(config.base)
    .pipe(plugins.webserver({
        host: '0.0.0.0', 
        port: process.env.PORT,
        livereload: false,
        open: false
    }));
});

gulp.task('callback-example', function(callback) {
    // Use the callback in the async function
    fs.readFile('...', function(err, file) {
        console.log(file);
        callback();
//      ^^^^^^^^^^
//       This is what lets gulp know this task is complete!
    });
});
gulp.task('browserify', ['clean'], function(cb) {
    return gulp.src('./src/PathFinding.js')
    .pipe(browserify({ standalone: 'PF' }))
    .pipe(rename('pathfinding-browserified.js'))
    .pipe(gulp.dest('./lib/'), cb);
});

gulp.task('uglify', ['browserify'], function(cb) {
    return gulp.src('./lib/pathfinding-browserified.js')
    .pipe(uglify())
    .pipe(rename('pathfinding-browser.min.js'))
    .pipe(gulp.dest('./lib/'), cb);
});
gulp.task('heroku:production', function(){
  runSeq('clean', 'build', 'minify')
});
gulp.task('scripts', ['clean', 'browserify', 'uglify'], function(cb) {
    return gulp.src(['./src/banner', './lib/pathfinding-browserified.js'])
    .pipe(concat('pathfinding-browser.js'))
    .pipe(gulp.dest('./lib/'), cb);
});

gulp.task('compile', ['scripts'], function() {
    del('./lib/pathfinding-browserified.js');
});

gulp.task('test', function () {
    return gulp.src('./test/**/*.js', {read: false})
        .pipe(mocha({reporter: 'spec', bail: true, globals: { should: require('should') }}));
});

gulp.task('bench', function() {
    shell.exec('node benchmark/benchmark.js');
});

gulp.task('lint', function() {
  return gulp.src('./src/**/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter(stylish))
    .pipe(jshint.reporter('fail'));
});

gulp.task('release', ['compile'], function(cb) {
  inquirer.prompt({
      type: 'list',
      name: 'bumpType',
      message: 'Which version do you want to bump?',
      choices: ['patch', 'minor', 'major'],
      //default is patch
      default: 0
    }, function (result) {
      var f = jsonfile.readFileSync('./package.json');
      f.version = semver.inc(f.version, result.bumpType);
      jsonfile.writeFileSync('./package.json', f);

      shell.exec('git add .');
      shell.exec('git commit -m "Bumping version to ' + f.version + '"');
      shell.exec('git push origin master');
      shell.exec('git tag -a ' + f.version + ' -m "Creating tag for version ' + f.version + '"');
      shell.exec('git push origin ' + f.version);
      shell.exec('npm publish');

      shell.exec('git clone https://github.com/imor/pathfinding-bower.git release');
      process.chdir('release');
      fs.writeFileSync('pathfinding-browser.js', fs.readFileSync('../lib/pathfinding-browser.js'));
      fs.writeFileSync('pathfinding-browser.min.js', fs.readFileSync('../lib/pathfinding-browser.min.js'));

      f = jsonfile.readFileSync('bower.json');
      f.version = semver.inc(f.version, result.bumpType);
      jsonfile.writeFileSync('bower.json', f);

      shell.exec('git add .');
      shell.exec('git commit -m "Bumping version to ' + f.version + '"');
      shell.exec('git push origin master');
      shell.exec('git tag -a ' + f.version + ' -m "Creating tag for version ' + f.version + '"');
      shell.exec('git push origin ' + f.version);

      process.chdir('../');
      del('release');
      del('lib/**/*.*', cb);
    });
});

gulp.task('default', ['lint', 'test', 'compile'], function() {
});
