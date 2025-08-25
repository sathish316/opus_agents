"""
Common data models for the financial planner system.
"""

from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"


class FundCategory(str, Enum):
    EQUITY = "EQUITY"
    DEBT = "DEBT"
    HYBRID = "HYBRID"
    GOLD = "GOLD"
    SILVER = "SILVER"


class RiskProfile(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"


class AgeGroup(str, Enum):
    YOUNG_0_20 = "0-20"
    YOUNG_ADULT_20_30 = "20-30"
    ADULT_30_40 = "30-40"
    MIDDLE_AGE_40_50 = "40-50"
    PRE_RETIREMENT_50_60 = "50-60"
    SENIOR_60_PLUS = "60+"


class Transaction(BaseModel):
    date: datetime
    fund_code: str
    fund_name: str
    transaction_type: TransactionType
    transaction_count: float  # Number of units or amount


class Fund(BaseModel):
    code: str
    name: str
    category: FundCategory
    nav: Optional[float] = None
    current_price: Optional[float] = None


class PortfolioData(BaseModel):
    transactions: List[Transaction]
    funds: Dict[str, Fund]
    total_investment: float = 0.0
    current_value: float = 0.0


class XIRRResult(BaseModel):
    fund_code: str
    fund_name: str
    xirr: float
    category: FundCategory
    total_invested: float
    current_value: float


class Recommendation(BaseModel):
    agent_name: str
    category: FundCategory
    current_xirr: float
    optimal_xirr: float
    recommendation: str
    recommended_funds: List[str]
    action_required: bool


class PortfolioAnalysis(BaseModel):
    portfolio_summary: Dict[str, float]
    xirr_results: List[XIRRResult]
    recommendations: List[Recommendation]
    overall_score: float
    risk_assessment: str