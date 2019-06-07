// Gulpとプラグイン読み込み
const gulp = require('gulp');
//const webserver = require('gulp-webserver');
const sass = require('gulp-sass');
const pug = require('gulp-pug');
const exec = require('child_process').exec;

// `sass`タスク
// bulma.sassをbulma.cssに変換
gulp.task('sass', function(done) {
  gulp.src('./src/bulma-0.7.4/bulma.sass')
    .pipe(sass({outputStyle: 'expanded'}))
    .pipe(gulp.dest('./static/css/'));
  // Gulp4系では、callback関数`done`を最後に呼び出さないと正常終了しない
  done();
});

// `sass-watch`タスク
// sassファイルを監視し、`sass`タスクを実行する
gulp.task('sass-watch', function(done) {
  // Gulp4系では、タスクウォッチャの引数が ['タスク名'] => gulp.task('タスク名') に変更
  // 複数のタスクを引数に入れる場合は gulp.series('タスク1', ...) or gulp.parallel('タスク1', ...)
  var watcher = gulp.watch('./src/bulma-0.7.4/**/*.sass', gulp.task('sass'));
  watcher.on('change', function(event) {});
  
  // ウォッチャは実行し続けるため、doneを呼び出す必要はない
  //done();
});

// `pug`タスク
// pugをhtmlに変換
gulp.task('pug', function(done) {
  gulp.src('./src/pug/**/*.pug')
    .pipe(pug({pretty: true}))
    .pipe(gulp.dest('./html/'));
  done();
});

// `pug-watch`タスク
// pugファイルを監視し、`pug`タスクを実行する
gulp.task('pug-watch', function(done) {
  var watcher = gulp.watch('./src/pug/**/*.pug', gulp.task('pug'));
  watcher.on('change', function(event) {});
});

// `webserver`タスク
// python-flaskローカルサーバー(localhost:8000)公開
gulp.task('webserver', function(done) {
  exec('python server.py', function(err, stdout, stderr) {
    console.log(stdout);
    console.error(stderr);
  });
});

// gulpのローカルサーバーを使う場合は以下の通り
/*gulp.task('webserver', function(done) {
  gulp
    .src('./dist')
    .pipe(webserver({
      livereload: true, // 自動更新有効化
      open: true, // ブラウザで自動的に開く
      port: 8000, // ポート8000番を使用
    }));
});*/

// `apiserver`タスク
// ./api/app.pyを実行（ローカルAPIサーバー実行）
gulp.task('apiserver', function(done) {
  // flaskは localhost:5000 で実行される
  exec('python ./api/app.py', function(err, stdout, stderr) {
    console.log(stdout);
    console.error(stderr);
  });
});

// `default`タスク: gulpコマンドで呼び出されるタスク
// `sass-watch`, `pug-watch`, `webserver`, `apiserver`タスクを並列実行
gulp.task('default', gulp.parallel('sass-watch', 'pug-watch', 'webserver'/*, 'apiserver'*/));
