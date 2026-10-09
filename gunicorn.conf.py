"""Render/Linux向けの本番サーバー設定。"""
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
# 小規模なSQLiteアプリ用。DBへの同時書き込みを抑えます。
workers = 1
threads = 2
accesslog = "-"
errorlog = "-"
timeout = 30
