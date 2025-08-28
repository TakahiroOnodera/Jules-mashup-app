import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む（ローカル開発用）
# Cloud Runなどの環境では、環境変数はサービスの設定から直接注入される
load_dotenv()

# 環境変数からAPIキーを取得
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
