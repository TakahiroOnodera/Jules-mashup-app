import httpx
import logging
from typing import List, Optional

from .config import WEATHER_API_KEY, NEWS_API_KEY
from .models import WeatherInfo, NewsArticle

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 仙台市の緯度・経度
SENDAI_LAT = 38.2682
SENDAI_LON = 140.8694

async def fetch_weather(client: httpx.AsyncClient) -> Optional[WeatherInfo]:
    """OpenWeatherMap APIから現在の仙台市の天気を取得する"""
    if not WEATHER_API_KEY:
        logger.warning("Weather APIキーが設定されていません。")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": SENDAI_LAT,
        "lon": SENDAI_LON,
        "appid": WEATHER_API_KEY,
        "units": "metric",  # 温度を摂氏で取得
        "lang": "ja",       # 説明を日本語で取得
    }

    try:
        response = await client.get(url, params=params)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        data = response.json()

        # APIレスポンスから必要な情報を抽出し、モデルに変換
        return WeatherInfo(
            description=data["weather"][0]["description"],
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            icon_id=data["weather"][0]["icon"],
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"天気情報の取得でHTTPエラーが発生しました: {e.response.status_code} - {e.response.text}")
        return None
    except (httpx.RequestError, KeyError, IndexError) as e:
        logger.error(f"天気情報の取得中にエラーが発生しました: {e}")
        return None


async def fetch_news(client: httpx.AsyncClient) -> Optional[List[NewsArticle]]:
    """NewsAPI.orgから仙台に関連する日本のニュースを取得する"""
    if not NEWS_API_KEY:
        logger.warning("News APIキーが設定されていません。")
        return None

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "country": "jp",
        "q": "仙台",
        "pageSize": 5,  # 記事数を5件に制限
    }

    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        articles = [
            NewsArticle(
                title=article["title"],
                source_name=article["source"]["name"],
                url=article["url"],
                published_at=article["publishedAt"],
            )
            for article in data["articles"]
        ]
        return articles
    except httpx.HTTPStatusError as e:
        logger.error(f"ニュース情報の取得でHTTPエラーが発生しました: {e.response.status_code} - {e.response.text}")
        return None
    except (httpx.RequestError, KeyError) as e:
        logger.error(f"ニュース情報の取得中にエラーが発生しました: {e}")
        return None
