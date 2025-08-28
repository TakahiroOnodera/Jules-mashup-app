from pydantic import BaseModel, Field
from typing import List, Optional

class WeatherInfo(BaseModel):
    """現在の天気情報"""
    description: str = Field(..., description="天気概要（例: 晴れ）")
    temperature: float = Field(..., description="気温（摂氏）")
    humidity: int = Field(..., description="湿度（%）")
    icon_id: str = Field(..., description="天気を表すアイコンID")

class NewsArticle(BaseModel):
    """ニュース記事の情報"""
    title: str = Field(..., description="記事のタイトル")
    source_name: str = Field(..., description="ニュース提供元")
    url: str = Field(..., description="記事のURL")
    published_at: str = Field(..., description="公開日時 (ISO 8601形式)")

class SendaiInfoResponse(BaseModel):
    """APIレスポンスの全体構造"""
    weather: Optional[WeatherInfo] = Field(None, description="現在の天気情報")
    news: Optional[List[NewsArticle]] = Field(None, description="最新ニュースのリスト")
