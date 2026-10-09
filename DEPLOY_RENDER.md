# masa-cafe：Renderへの公開準備

このフォルダがGitHubのmasa-cafeリポジトリのルートです。
今回行ったのはファイルの準備だけです。登録・認証・デプロイ・commit・pushは実行していません。

## 追加・変更したファイル

- requirements.txt：Flask（Webアプリ）とGunicorn（本番用Webサーバー）の依存一覧。sqlite3はPython標準機能なので追加不要です。
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

同梱render.yamlは無料の動作確認用です。Renderの通常のファイル領域は一時的なため、再起動・再デプロイでお問い合わせのSQLiteデータが失われます。
実運用で保存を継続するには、後日有料Web ServiceにPersistent Diskを追加し、次のように設定してください（今回作成・契約はしていません）。

- DiskのMount Path：`/var/data`
- 環境変数DATABASE_PATH：`/var/data/cafe.db`

DBの初期化はディスクを使える起動時に行います。ローカルの既存cafe.dbは自動転送されません。既存データを引き継ぐ場合は別途移行が必要です。

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
既存のローカルFlask環境のテストクライアントで、静的ファイル配信・お問い合わせ保存・DB接続終了・不正JSONの400・非公開ファイルの404・PORT設定を確認しました。既存cafe.dbは使わず、一時DBで検証しています。新しい依存一覧のインストール、Linux上のGunicorn実起動、Render上の動作は未検証です。
