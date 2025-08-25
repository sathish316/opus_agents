"""
Gold/Silver Fund Manager Agent - Analyzes and provides recommendations for precious metal funds.
"""

from mock_agent import Agent
from pydantic import BaseModel
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Transaction, Fund, FundCategory, Recommendation, XIRRResult
from utils import calculate_xirr, get_benchmark_xirr, get_marquee_funds


class GoldSilverAnalysisResult(BaseModel):
    category: str = "GOLD_SILVER"
    funds_analyzed: int
    total_invested: float
    current_value: float
    portfolio_xirr: float
    benchmark_xirr: float
    gold_allocation: float
    silver_allocation: float
    recommendation: str
    recommended_funds: List[str]
    action_required: bool


# Create the Gold/Silver Fund Manager agent
gold_silver_fund_manager = Agent(
    'openai:gpt-4o-mini',
    result_type=GoldSilverAnalysisResult,
    system_prompt="""
    You are an expert Gold/Silver Fund Manager specializing in Indian precious metal investments.
    
    Your responsibilities:
    1. Filter and analyze gold and silver funds from the portfolio
    2. Calculate XIRR for precious metal investments
    3. Compare performance against benchmarks (8% for gold, 9% for silver)
    4. Recommend optimal 50:50 gold-silver allocation
    5. Suggest marquee precious metal funds for portfolio hedging
    
    Key metrics for precious metals in India:
    - Expected minimum XIRR Gold: 8%
    - Expected minimum XIRR Silver: 9%
    - Optimal allocation: 50% Gold, 50% Silver
    - Recommended funds: Nippon Gold Savings, HDFC Gold, Kotak Silver ETF
    
    Precious metals serve as portfolio hedges against inflation and currency devaluation.
    Focus on long-term wealth preservation and diversification benefits.
    """,
)


def analyze_gold_silver_portfolio(transactions: List[Transaction], funds: Dict[str, Fund]) -> GoldSilverAnalysisResult:
    """
    Analyze gold/silver portion of the portfolio.
    
    Args:
        transactions: All portfolio transactions
        funds: Fund details dictionary
        
    Returns:
        GoldSilverAnalysisResult with analysis and recommendations
    """
    # Filter gold and silver transactions
    gold_silver_transactions = [
        txn for txn in transactions 
        if funds.get(txn.fund_code, {}).category in [FundCategory.GOLD, FundCategory.SILVER]
    ]
    
    if not gold_silver_transactions:
        return GoldSilverAnalysisResult(
            funds_analyzed=0,
            total_invested=0.0,
            current_value=0.0,
            portfolio_xirr=0.0,
            benchmark_xirr=8.5,  # Average of gold and silver
            gold_allocation=0.0,
            silver_allocation=0.0,
            recommendation="No precious metal funds found. Consider adding gold/silver in 50:50 ratio for portfolio hedging.",
            recommended_funds=get_marquee_funds(FundCategory.GOLD) + get_marquee_funds(FundCategory.SILVER),
            action_required=True
        )
    
    # Group transactions by fund and category
    gold_transactions = {}
    silver_transactions = {}
    
    for txn in gold_silver_transactions:
        fund = funds[txn.fund_code]
        if fund.category == FundCategory.GOLD:
            if txn.fund_code not in gold_transactions:
                gold_transactions[txn.fund_code] = []
            gold_transactions[txn.fund_code].append(txn)
        elif fund.category == FundCategory.SILVER:
            if txn.fund_code not in silver_transactions:
                silver_transactions[txn.fund_code] = []
            silver_transactions[txn.fund_code].append(txn)
    
    # Calculate XIRR for gold and silver separately
    total_invested = 0.0
    current_value = 0.0
    gold_invested = 0.0
    silver_invested = 0.0
    xirr_results = []
    
    # Process gold funds
    for fund_code, fund_txns in gold_transactions.items():
        fund = funds[fund_code]
        fund_xirr = calculate_xirr(fund_txns, fund.current_price or 100.0)
        
        invested = sum(txn.transaction_count for txn in fund_txns if txn.transaction_type.value == "BUY")
        current_val = invested * (fund.current_price or 100.0) / 100.0
        
        gold_invested += invested
        total_invested += invested
        current_value += current_val
        
        xirr_results.append(XIRRResult(
            fund_code=fund_code,
            fund_name=fund.name,
            xirr=fund_xirr,
            category=FundCategory.GOLD,
            total_invested=invested,
            current_value=current_val
        ))
    
    # Process silver funds
    for fund_code, fund_txns in silver_transactions.items():
        fund = funds[fund_code]
        fund_xirr = calculate_xirr(fund_txns, fund.current_price or 100.0)
        
        invested = sum(txn.transaction_count for txn in fund_txns if txn.transaction_type.value == "BUY")
        current_val = invested * (fund.current_price or 100.0) / 100.0
        
        silver_invested += invested
        total_invested += invested
        current_value += current_val
        
        xirr_results.append(XIRRResult(
            fund_code=fund_code,
            fund_name=fund.name,
            xirr=fund_xirr,
            category=FundCategory.SILVER,
            total_invested=invested,
            current_value=current_val
        ))
    
    # Calculate allocations
    gold_allocation = (gold_invested / total_invested * 100) if total_invested > 0 else 0.0
    silver_allocation = (silver_invested / total_invested * 100) if total_invested > 0 else 0.0
    
    # Calculate weighted average XIRR
    if total_invested > 0:
        portfolio_xirr = sum(result.xirr * result.total_invested for result in xirr_results) / total_invested
    else:
        portfolio_xirr = 0.0
    
    benchmark_xirr = 8.5  # Average of gold (8%) and silver (9%)
    recommended_funds = get_marquee_funds(FundCategory.GOLD) + get_marquee_funds(FundCategory.SILVER)
    
    # Prepare analysis context for LLM
    analysis_context = f"""
    Gold/Silver Portfolio Analysis:
    - Number of precious metal funds: {len(gold_transactions) + len(silver_transactions)}
    - Total invested: ₹{total_invested:,.2f}
    - Current value: ₹{current_value:,.2f}
    - Portfolio XIRR: {portfolio_xirr:.2f}%
    - Benchmark XIRR: {benchmark_xirr:.2f}%
    - Gold allocation: {gold_allocation:.1f}%
    - Silver allocation: {silver_allocation:.1f}%
    - Optimal allocation: 50% Gold, 50% Silver
    
    Individual fund performance:
    {chr(10).join([f"- {result.fund_name} ({result.category.value}): {result.xirr:.2f}% XIRR" for result in xirr_results])}
    
    Recommended marquee funds: {', '.join(recommended_funds)}
    
    Please provide comprehensive precious metals analysis focusing on hedging and diversification benefits.
    """
    
    # Call the LLM agent for analysis
    result = gold_silver_fund_manager.run_sync(analysis_context)
    
    return GoldSilverAnalysisResult(
        funds_analyzed=len(gold_transactions) + len(silver_transactions),
        total_invested=total_invested,
        current_value=current_value,
        portfolio_xirr=portfolio_xirr,
        benchmark_xirr=benchmark_xirr,
        gold_allocation=gold_allocation,
        silver_allocation=silver_allocation,
        recommendation=result.data.recommendation,
        recommended_funds=recommended_funds,
        action_required=portfolio_xirr < benchmark_xirr or abs(gold_allocation - 50.0) > 15.0
    )