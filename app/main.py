import asyncio
import httpx
import logging
from fastapi import FastAPI, HTTPException

from .models import SendaiInfoResponse
from .services import fetch_weather, fetch_news

# ロガーの取得
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sendai Info API",
    description="仙台市の天気とニュース情報を提供するAPIです。",
    version="1.0.0",
)

@app.get("/api/sendai-info", response_model=SendaiInfoResponse)
async def get_sendai_info():
    """
    仙台市の現在の天気と、関連する最新ニュースをまとめて取得します。
    """
    async with httpx.AsyncClient() as client:
        # 天気情報とニュース情報の取得タスクを作成
        weather_task = fetch_weather(client)
        news_task = fetch_news(client)

        # asyncio.gatherでタスクを並列実行
        # return_exceptions=True にすることで、片方のタスクが失敗しても例外を送出せず、結果が格納される
        results = await asyncio.gather(
            weather_task,
            news_task,
            return_exceptions=True
        )

    # 結果を検証し、例外が発生した場合はNoneを設定
    weather_data = results[0] if not isinstance(results[0], Exception) else None
    news_data = results[1] if not isinstance(results[1], Exception) else None

    # 例外が発生した場合、ログに出力
    if isinstance(results[0], Exception):
        logger.error(f"天気情報の取得に失敗しました: {results[0]}", exc_info=results[0])
    if isinstance(results[1], Exception):
        logger.error(f"ニュース情報の取得に失敗しました: {results[1]}", exc_info=results[1])

    # 両方のデータソースから情報を取得できなかった場合、503エラーを返す
    if weather_data is None and news_data is None:
        raise HTTPException(
            status_code=503,
            detail="全ての外部サービスから情報を取得できませんでした。"
        )

    # 成功したデータをレスポンスとして返す
    return SendaiInfoResponse(weather=weather_data, news=news_data)

@app.get("/")
async def read_root():
    return {"message": "Sendai Info APIへようこそ！ドキュメントは /docs をご覧ください。"}
