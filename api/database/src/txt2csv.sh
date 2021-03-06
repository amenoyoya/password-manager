#!/bin/bash

# テキストファイルをCSVに変換
## - テキストファイル フォーマット:
##    <サービス名> (空白2つ以上) <ユーザー名> (空白2つ以上) <パスワード> (空白2つ以上) <備考>
## - CSV フォーマット:
##    "<サービス名>","<ユーザー名>","<パスワード>","<備考>"

# 解説
## sedの置換パターンは '' で囲むため、エスケープシーケンスは2つ続ける
## 拡張正規表現（{n,m}: 直前のパターンのn回以上, m回以下の繰り返し 等）を使う場合は `-r` オプションをつける
## - 's/\\/\\\\/g': `\` を `\\` に置換 (global)
## - 's/"/\\"/g': `\` を `\\` に置換 (global)
## - 's/ {2,}/","/g': 2つ以上のスペースを `","` に置換 (global)
## - 's/^/"/': 先頭を `"` に置換 
## - 's/$/"/': 最後尾を `"` に置換 

sed 's/\\/\\\\/g' "$1" | sed 's/"/\\"/g' | sed -r 's/ {2,}/","/g' | sed 's/^/"/' | sed 's/$/"/' > "$1.csv"
