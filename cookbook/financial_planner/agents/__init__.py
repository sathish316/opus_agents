"""
Financial Planner Agents Package

This package contains specialized PydanticAI agents for portfolio analysis:
- EquityFundManager: Analyzes equity funds performance
- DebtFundManager: Analyzes debt funds performance  
- HybridFundManager: Analyzes hybrid funds performance
- GoldSilverFundManager: Analyzes precious metals funds
- RatioAnalyzer: Analyzes asset allocation ratios
"""

from .equity_fund_manager import analyze_equity_portfolio
from .debt_fund_manager import analyze_debt_portfolio
from .hybrid_fund_manager import analyze_hybrid_portfolio
from .gold_silver_fund_manager import analyze_gold_silver_portfolio
from .ratio_analyzer import analyze_portfolio_ratios

__all__ = [
    'analyze_equity_portfolio',
    'analyze_debt_portfolio', 
    'analyze_hybrid_portfolio',
    'analyze_gold_silver_portfolio',
    'analyze_portfolio_ratios'
]