# masa-cafe：Renderへの公開準備

このフォルダがGitHubのmasa-cafeリポジトリのルートです。
今回行ったのはファイルの準備だけです。登録・認証・デプロイ・commit・pushは実行していません。

## 追加・変更したファイル

- requirements.txt：Flask（Webアプリ）、Gunicorn（本番用Webサーバー）、psycopg[binary]（PostgreSQL接続用）の依存一覧。sqlite3はPython標準機能なので追加不要です。
- gunicorn.conf.py：RenderのPORTに合わせて0.0.0.0で待ち受け、ログを標準出力へ送ります。SQLiteを使う小規模構成として1ワーカー・2スレッドです。
- render.yaml：Renderのビルド・起動コマンドを記録した設定。無料の試用構成で、自動デプロイは無効です。このファイルを保存しただけでは公開されません。
- server.py：Gunicorn起動時にもDBを初期化し、保存先をDATABASE_PATHで指定できるようにしました。HTML/CSS/JSだけを配信し、DBやソースコードの公開を防ぎます。不正なJSONには400を返します。正常なお問い合わせの保存・成功レスポンスは維持しています。ローカルのdebugは初期状態で無効です。
- .gitignore：Pythonの一時ファイル・仮想環境・.env・SQLiteの補助ファイルをGit管理から除外します。

既存のindex.html、style.css、script.jsとcafe.dbの内容は変更していません。

## 後日Renderで使う設定（今回は操作していません）

| 項目 | 設定 |
| --- | --- |
| 種類 | Web Service |
| 言語 | Python 3 |
| Root Directory | 空欄（masa-cafeリポジトリのルート） |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn --config gunicorn.conf.py server:app` |
| Health Check Path | `/` |
| Auto Deploy | Off |

Gunicornはserver.pyのappを読み込みます。Flask開発サーバーの`python server.py`を本番起動には使いません。
この親フォルダ「右腕AI」をリポジトリにする場合は、Root Directoryを「店舗サイト」に変更する必要があります。

## お問い合わせデータの保存について

2026-10-10の変更で、保存先を起動時の環境変数で切り替えます。

- `DATABASE_URL` が未設定・空欄：従来どおりSQLite。保存先は `DATABASE_PATH`、省略時はこのフォルダの `cafe.db`。
- `DATABASE_URL` が設定済み：PostgreSQL。`DATABASE_PATH` は使いません。接続失敗時もSQLiteに切り替えずエラーにします。
- 起動時にcontactsテーブルを作成し、保存成功時は変更を確定、失敗時は取り消して接続を閉じます。既存テーブルやデータは削除しません。
- `/api/contacts` は従来の配列形式 `[id, name, message]` を維持し、ID順に返します。

Renderでは作成済み `masa-cafe-db` のInternal Database URLを `masa-cafe` の環境変数 `DATABASE_URL` に設定します。秘密の値をソース、render.yaml、Git、説明書へ貼り付けないでください。render.yamlは変更していないため、これだけではDB接続は設定されません。

ローカルの既存cafe.dbは自動転送されません。既存データを引き継ぐ場合は別途移行が必要です。RenderでDATABASE_URLを未設定のまま使うと一時的なSQLiteになり、再デプロイ等でデータが失われる可能性があります。

## 次の公開作業（ユーザーの明示了承後に実施）

1. 今回の差分とテスト結果を確認します。
2. 了承後にGit commit / pushを実施します。Renderの自動デプロイ設定も確認します。
3. Render側で入力済みのDATABASE_URLを保存し、新しいコードと依存をデプロイします。保存操作がデプロイを起動する可能性があるため、ここも了承後に行います。
4. 起動成功・テスト問い合わせの保存と一覧取得を確認します。本番へのテスト書き込みも了承後に行います。

今回の作業では、上記の外部操作は実施していません。

## Windowsでローカル確認

このフォルダ内で次を実行します。仮想環境は他のPythonプロジェクトと依存を分けるためのものです。

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python server.py
```

ブラウザで http://127.0.0.1:5000/ を開きます。
Gunicornの実起動はLinux向けです。WindowsではFlaskのテストクライアントでサイト配信・API・DB保存を確認できます。
開発デバッグが必要な場合だけ、起動前に`$env:FLASK_DEBUG="1"`を指定してください。

参考：
- https://render.com/docs/deploy-flask
- https://render.com/docs/disks
- https://render.com/docs/blueprint-spec

## 今回の確認範囲
2026-10-10: `test_server.py` のローカルテストで、一時SQLiteへの保存・一覧取得・再読込後の保持・連番・日本語と引用符を含む入力・失敗時の取り消しと接続終了・不正JSONの400・非公開ファイルの404を確認。PostgreSQLは実ドライバを読み込み、接続の代役（モック）で初期化・INSERT・SELECT・確定・取り消し・接続終了・接続失敗時にSQLiteへ切り替えないことを確認しました。

再実行: 依存のインストール後、このフォルダで `python -m unittest discover -s . -p test_server.py -v`。本番URLは使用せず、一時DBとモックのみ使います。

PostgreSQL実サーバー、Linux上のGunicorn実起動、Render上での動作は未検証です。既存cafe.dbにはテストデータを書き込んでいません。

ドライバの参考: https://www.psycopg.org/psycopg3/docs/basic/usage.html
