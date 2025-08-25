"""
Debt Fund Manager Agent - Analyzes and provides recommendations for debt funds.
"""

from mock_agent import Agent
from pydantic import BaseModel
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Transaction, Fund, FundCategory, Recommendation, XIRRResult
from utils import calculate_xirr, get_benchmark_xirr, get_marquee_funds


class DebtAnalysisResult(BaseModel):
    category: str = "DEBT"
    funds_analyzed: int
    total_invested: float
    current_value: float
    portfolio_xirr: float
    benchmark_xirr: float
    recommendation: str
    recommended_funds: List[str]
    action_required: bool


# Create the Debt Fund Manager agent
debt_fund_manager = Agent(
    'openai:gpt-4o-mini',
    result_type=DebtAnalysisResult,
    system_prompt="""
    You are an expert Debt Fund Manager specializing in Indian debt mutual funds.
    
    Your responsibilities:
    1. Filter and analyze only debt-based funds from the portfolio
    2. Calculate XIRR for debt investments
    3. Compare performance against benchmark (7.5% for debt)
    4. Recommend marquee debt/liquid funds if performance is below optimal
    5. Provide clear, actionable recommendations for capital preservation and steady returns
    
    Key metrics for debt funds in India:
    - Expected minimum XIRR: 7.5%
    - Recommended marquee funds: SBI Magnum Gilt, HDFC Short Term Debt, ICICI Liquid Fund
    
    Focus on capital preservation, liquidity, and steady income generation.
    Always provide specific, risk-aware recommendations.
    """,
)


def analyze_debt_portfolio(transactions: List[Transaction], funds: Dict[str, Fund]) -> DebtAnalysisResult:
    """
    Analyze debt portion of the portfolio.
    
    Args:
        transactions: All portfolio transactions
        funds: Fund details dictionary
        
    Returns:
        DebtAnalysisResult with analysis and recommendations
    """
    # Filter debt transactions
    debt_transactions = [
        txn for txn in transactions 
        if funds.get(txn.fund_code, {}).category == FundCategory.DEBT
    ]
    
    if not debt_transactions:
        return DebtAnalysisResult(
            funds_analyzed=0,
            total_invested=0.0,
            current_value=0.0,
            portfolio_xirr=0.0,
            benchmark_xirr=get_benchmark_xirr(FundCategory.DEBT),
            recommendation="No debt funds found in portfolio. Consider adding debt exposure for stability.",
            recommended_funds=get_marquee_funds(FundCategory.DEBT),
            action_required=True
        )
    
    # Group transactions by fund
    fund_transactions = {}
    for txn in debt_transactions:
        if txn.fund_code not in fund_transactions:
            fund_transactions[txn.fund_code] = []
        fund_transactions[txn.fund_code].append(txn)
    
    # Calculate XIRR for each debt fund
    total_invested = 0.0
    current_value = 0.0
    xirr_results = []
    
    for fund_code, fund_txns in fund_transactions.items():
        fund = funds[fund_code]
        fund_xirr = calculate_xirr(fund_txns, fund.current_price or 100.0)
        
        invested = sum(txn.transaction_count for txn in fund_txns if txn.transaction_type.value == "BUY")
        current_val = invested * (fund.current_price or 100.0) / 100.0  # Simplified calculation
        
        total_invested += invested
        current_value += current_val
        
        xirr_results.append(XIRRResult(
            fund_code=fund_code,
            fund_name=fund.name,
            xirr=fund_xirr,
            category=FundCategory.DEBT,
            total_invested=invested,
            current_value=current_val
        ))
    
    # Calculate weighted average XIRR
    if total_invested > 0:
        portfolio_xirr = sum(result.xirr * result.total_invested for result in xirr_results) / total_invested
    else:
        portfolio_xirr = 0.0
    
    benchmark_xirr = get_benchmark_xirr(FundCategory.DEBT)
    recommended_funds = get_marquee_funds(FundCategory.DEBT)
    
    # Prepare analysis context for LLM
    analysis_context = f"""
    Debt Portfolio Analysis:
    - Number of debt funds: {len(fund_transactions)}
    - Total invested: ₹{total_invested:,.2f}
    - Current value: ₹{current_value:,.2f}
    - Portfolio XIRR: {portfolio_xirr:.2f}%
    - Benchmark XIRR: {benchmark_xirr:.2f}%
    - Performance gap: {portfolio_xirr - benchmark_xirr:.2f}%
    
    Individual fund performance:
    {chr(10).join([f"- {result.fund_name}: {result.xirr:.2f}% XIRR" for result in xirr_results])}
    
    Recommended marquee funds: {', '.join(recommended_funds)}
    
    Please provide a comprehensive debt fund analysis focusing on capital preservation and steady returns.
    """
    
    # Call the LLM agent for analysis
    result = debt_fund_manager.run_sync(analysis_context)
    
    return DebtAnalysisResult(
        funds_analyzed=len(fund_transactions),
        total_invested=total_invested,
        current_value=current_value,
        portfolio_xirr=portfolio_xirr,
        benchmark_xirr=benchmark_xirr,
        recommendation=result.data.recommendation,
        recommended_funds=recommended_funds,
        action_required=portfolio_xirr < benchmark_xirr
    )