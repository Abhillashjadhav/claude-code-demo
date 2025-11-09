"""Data models for stock screener"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Stock:
    """Stock model with valuation metrics"""
    ticker: str
    name: str
    sector: str
    market_cap: float  # in billions
    price: float
    pe_ratio: Optional[float]
    ps_ratio: Optional[float]
    pb_ratio: Optional[float]
    ev_ebitda: Optional[float]
    revenue_growth: float  # percentage
    earnings_growth: float  # percentage
    sentiment_score: float  # -1 to 1
    sentiment_trend: str  # "up", "down", "stable"
    management_guidance: str  # "positive", "neutral", "negative"
    volume: int
    last_updated: str

    def to_dict(self):
        return {
            'ticker': self.ticker,
            'name': self.name,
            'sector': self.sector,
            'market_cap': self.market_cap,
            'price': self.price,
            'pe_ratio': self.pe_ratio,
            'ps_ratio': self.ps_ratio,
            'pb_ratio': self.pb_ratio,
            'ev_ebitda': self.ev_ebitda,
            'revenue_growth': self.revenue_growth,
            'earnings_growth': self.earnings_growth,
            'sentiment_score': self.sentiment_score,
            'sentiment_trend': self.sentiment_trend,
            'management_guidance': self.management_guidance,
            'volume': self.volume,
            'last_updated': self.last_updated
        }

@dataclass
class ScreenerFilter:
    """Filter criteria for stock screening"""
    min_market_cap: Optional[float] = None
    max_market_cap: Optional[float] = None
    min_pe_ratio: Optional[float] = None
    max_pe_ratio: Optional[float] = None
    min_ps_ratio: Optional[float] = None
    max_ps_ratio: Optional[float] = None
    min_revenue_growth: Optional[float] = None
    min_sentiment_score: Optional[float] = None
    sectors: Optional[List[str]] = None
    management_guidance: Optional[str] = None
