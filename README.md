# SQL contest tool

[TOPSIC sql contest](https://topsic-contest.jp/) の問題を手元で解くための環境を作る非公式ツールです。  
作成されたDBにお好きなSQLite I/Fでアクセスし、好きなSQLフォーマッタを使うことができます。  
おすすめはVSCode拡張の[SQLite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)です。  

- init
config.iniを生成します。SQLコンテストのユーザー名とパスワードなどを記録します。(未実装)
- init-problem(ip)
各問題ごとにSQLiteDBを作成し、問題ページ内のテーブル定義に則ってサンプルデータのテーブルを作成します。  
- init-contest(ic)
あるコンテストに対して各問題ごとにSQLiteDBを作成し、問題ページ内のテーブル定義に則ってサンプルデータのテーブルを作成します。  
- get-contests(gc)
コンテスト一覧を取得します。
- submit
問題に対して、回答を提出します。


## note
問題にtypoがあった場合やフォーマットが変わった場合(2022/08/09時点)、ツールが正常に動作しない可能性があります。  
適宜src下スクリプトを修正して使用してください。  

## usage
リポジトリのトップディレクトリにconfig.iniを作成し、以下のフォーマットに従ってユーザー名とパスワードを記述してください。
```
[user]
user_name = {SQLコンテストのユーザー名}
password = {SQLコンテストのパスワード}
```

実行方法
```shell
pipenv install
# init-problem
pipenv run python src/sql_contest_tool.py ip -c {コンテスト名} -p {問題コード}
# init-contest
pipenv run python src/sql_contest_tool.py ic -c {コンテスト名}
# submit
pipenv run python src/sql_contest_tool.py s -c {コンテスト名} -p {問題コード} -f {SQLファイルのパス}
# get-contests
pipenv run python src/sql_contest_tool.py gc
```

例: [練習用コンテスト問題1](https://topsic-contest.jp/contests/practice/problems/practice001)
```shell
pipenv run python src/sql_contest_tool.py ip -c practice -p practice001
```
contestディレクトリ下にpracticeディレクトリが生成され、その中にpractice001.dbが作られます。  