const path = require('path');

module.exports = {
    // 実行モード: develop => 開発, production => 本番
    // webpack4系以降はmodeを指定しないと警告が出る
    mode: 'development',
    // エントリーポイント
    entry: './src/index.jsx',
    // 出力設定
    output: {
        // バンドル後のファイル名
        filename: 'bundle.js',
        // 出力先のパス（※絶対パスで指定すること）
        path: path.join(__dirname, 'public')
    },
    // ビルドしたJavaScriptにsource-mapを書き出す
    devtool: 'inline-soruce-map',
    // モジュール設定
    module: {
        rules: [
            {
                // .js, .jsx ファイルを babel-loader でトランスコンパイル
                test: /\.js(x?)$/,
                exclude: /node_modules/, // node_modules/ 内のファイルは除外
                loader: 'babel-loader',
                // Babel のオプションを指定
                options: {
                    // preset_env, react の構文拡張を有効に
                    presets: [
                        ["@babel/preset-env"],
                        ["@babel/react"]
                    ]
                }
            },
            {
                // .css ファイル: css-loader => style-loader の順に適用
                // - css-loader: cssをJSにトランスコンパイル
                // - style-loader: <link>タグにスタイル展開
                test: /\.css$/,
                use: [
                    "style-loader",
                    {
                        loader: "css-loader",
                        options: { url: false }
                    }
                ]
            }
        ]
    },
    // 開発サーバー設定
    devServer: {
        /*historyApiFallback: {
            index: 'index.html'
        },*/
        // 起点ディレクトリを public/ に設定
        contentBase: path.join(__dirname, 'public'),
        // ポートを3000に設定
        port: 3000,
        // ブラウザを自動的に開く
        open: true
    }
};
