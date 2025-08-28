# Sendai Info API

これは、Flutterで開発される仙台市情報アプリ向けのバックエンドAPIです。
外部のAPIから仙台市の「天気」と「ニュース」の情報を取得し、まとめて単一のJSONレスポンスとして提供します。

## ✨ 主な特徴

- **FastAPI**: 高速でモダンなPythonウェブフレームワーク。
- **非同期処理**: `httpx` と `asyncio.gather` を活用し、外部APIへのリクエストを並列化して高速なレスポンスを実現。
- **堅牢な設計**: 片方の外部API（天気またはニュース）に障害が発生しても、もう片方のデータは返却します。
- **デプロイフレンドリー**: Google Cloud Runなどのコンテナ環境に簡単にデプロイ可能。

## ⚙️ セットアップ手順

### 1. リポジトリをクローン

```bash
git clone <repository_url>
cd sendai-info-api
```

### 2. 環境変数の設定

`.env.example` ファイルをコピーして `.env` ファイルを作成します。

```bash
cp .env.example .env
```

作成した `.env` ファイルを開き、ご自身のAPIキーを設定してください。

```dotenv
# .env

# OpenWeatherMap API Key
# https://home.openweathermap.org/api_keys
WEATHER_API_KEY="YOUR_OPENWEATHERMAP_API_KEY"

# NewsAPI.org API Key
# https://newsapi.org/account
NEWS_API_KEY="YOUR_NEWSAPI_ORG_API_KEY"
```

### 3. 依存関係のインストール

`requirements.txt` に記載されているライブラリをインストールします。

```bash
pip install -r requirements.txt
```

## 🚀 ローカルでの実行

以下のコマンドで、開発サーバーを起動します。

```bash
uvicorn app.main:app --reload
```

サーバーが起動したら、ブラウザで以下のURLにアクセスできます。

- **APIエンドポイント**: `http://127.0.0.1:8000/api/sendai-info`
- **自動生成ドキュメント (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **自動生成ドキュメント (ReDoc)**: `http://127.0.0.1:8000/redoc`

## 🐳 Dockerでの実行

ビルドして実行する場合:
```bash
docker build -t sendai-api .
docker run -p 8000:8000 --env-file .env sendai-api
```

## 📝 APIエンドポイント

### `GET /api/sendai-info`

仙台市の現在の天気と、関連する最新ニュース（最大5件）を取得します。

- **成功レスポンス (200 OK)**
  ```json
  {
    "weather": {
      "description": "晴れ",
      "temperature": 25.5,
      "humidity": 60,
      "icon_id": "01d"
    },
    "news": [
      {
        "title": "仙台市で新しいイベントが開催",
        "source_name": "河北新報",
        "url": "https://example.com/news/1",
        "published_at": "2023-10-27T10:00:00Z"
      }
    ]
  }
  ```

- **エラーレスポンス (503 Service Unavailable)**
  天気とニュースの両方の取得に失敗した場合。
  ```json
  {
    "detail": "全ての外部サービスから情報を取得できませんでした。"
  }
  ```
