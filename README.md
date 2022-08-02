# SQL contest tool

[TOPSIC sql contest](https://topsic-contest.jp/) の問題を手元で解くための環境を作るツール  
各問題ごとにSQLiteDBを作成し、問題ページ内のテーブル定義に則ってサンプルデータのテーブルを作成します。  

作成されたDBにお好きなSQLite I/Fでアクセスし、問題を解いてください。  
おすすめはVSCode拡張の[SQLite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)です。  

## usage
```shell
pipenv install
pipenv run python src/create_table_from_probrem.py {コンテスト名} {問題名}
```

例: [練習用コンテスト問題1](https://topsic-contest.jp/contests/practice/problems/practice001)
```shell
pipenv run python src/create_table_from_probrem.py practice practice001
```
contestディレクトリ下にpracticeディレクトリが生成され、その中にpractice001.dbが作られます。  