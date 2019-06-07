# パスワード管理サイト

## 開発環境構築

### 前提環境
- CLI:
  - node.js: `10.15.3 LTS`
    - パッケージマネージャ: `yarn`
- CSSフレームワーク:
  - bulma: `0.7.4`
- APIサーバー:
  - python: `3.6.7`
    - フレームワーク: `flask`

***

### Gulpインストール
タスクランナーとして`Gulp`を採用

```bash
# Gulpとプラグインをインストール
## Sassコンパイル用: gulp-sass
## Pugコンパイル用: gulp-pug
## ローカルサーバー用: gulp-webserver
$ yarn add -D gulp gulp-sass gulp-pug gulp-webserver

# Gulpバージョン確認
$ yarn gulp --version
CLI version: 2.2.0
Local version: 4.0.1 # Gulp4系を使用
```

`./gulpfile.js`にタスク記述

```javascript
// Gulpとプラグイン読み込み
const gulp = require('gulp');
const webserver = require('gulp-webserver');
const sass = require('gulp-sass');
const pug = require('gulp-pug');
const exec = require('child_process').exec;

// `sass`タスク
// bulma.sassをbulma.cssに変換
gulp.task('sass', function(done) {
  gulp.src('./bulma-0.7.4/bulma.sass')
    .pipe(sass({outputStyle: 'expanded'}))
    .pipe(gulp.dest('./dist/css/'));
  // Gulp4系では、callback関数`done`を最後に呼び出さないと正常終了しない
  done();
});

// `sass-watch`タスク
// sassファイルを監視し、`sass`タスクを実行する
gulp.task('sass-watch', function(done) {
  // Gulp4系では、タスクウォッチャの引数が ['タスク名'] => gulp.task('タスク名') に変更
  // 複数のタスクを引数に入れる場合は gulp.series('タスク1', ...) or gulp.parallel('タスク1', ...)
  var watcher = gulp.watch('./bulma-0.7.4/**/*.sass', gulp.task('sass'));
  watcher.on('change', function(event) {});
  
  // ウォッチャは実行し続けるため、doneを呼び出す必要はない
  //done();
});

// `pug`タスク
// pugをhtmlに変換
gulp.task('pug', function(done) {
  gulp.src('./pug/**/*.pug')
    .pipe(pug({pretty: true}))
    .pipe(gulp.dest('./dist/'));
  done();
});

// `pug-watch`タスク
// pugファイルを監視し、`pug`タスクを実行する
gulp.task('pug-watch', function(done) {
  var watcher = gulp.watch('./pug/**/*.pug', gulp.task('pug'));
  watcher.on('change', function(event) {});
});

// `webserver`タスク
// ./dist/ディレクトリをローカルサーバーで公開
gulp.task('webserver', function(done) {
  gulp
    .src('./dist')
    .pipe(webserver({
      livereload: true, // 自動更新有効化
      open: true, // ブラウザで自動的に開く
      port: 8000, // ポート8000番を使用
    }));
});

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
gulp.task('default', gulp.parallel('sass-watch', 'pug-watch', 'webserver', 'apiserver'));
```

以上の設定により `yarn gulp` でローカルサーバー（ファイル保存時にブラウザ自動更新）を実行できるようになる

また、並列的にPython(Flask)のAPIサーバーの起動, sassの自動コンパイルも行われる
