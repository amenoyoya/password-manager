# パスワード管理サイト

## 開発環境構築

### 前提環境
- CLI:
  - node.js: `10.15.3 LTS`
    - パッケージマネージャ: `yarn`
- CSSフレームワーク:
  - bulma: `0.7.4`

***

### Gulpインストール
タスクランナーとして`Gulp`を採用

```bash
# Gulpとプラグインをインストール
## Sassコンパイル用: gulp-sass
## ローカルサーバー用: gulp-webserver
$ yarn add -D gulp gulp-sass gulp-webserver

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

// `webserver`タスク
// ./dist/ディレクトリをローカルサーバーで公開
// `sass-watch`タスクも含める
gulp.task('webserver', function(done) {
  gulp
    .src('./dist')
    .pipe(webserver({
      livereload: true, // 自動更新有効化
      open: true, // ブラウザで自動的に開く
      port: 8000, // ポート8000番を使用
    }));
  
  // ローカルサーバーは実行し続けるため、doneを呼び出す必要はない
  //done();
});

// `default`タスク: gulpコマンドで呼び出されるタスク
// `sass-watch`, `webserver`タスクを並列実行
gulp.task('default', gulp.parallel('sass-watch', 'webserver'));
```

以上の設定により `yarn gulp` でローカルサーバー（ファイル保存時にブラウザ自動更新）を実行できるようになる

また、並列的にsassの自動コンパイルも行われる
