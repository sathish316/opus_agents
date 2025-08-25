"""
Ratio Analyzer Agent - Analyzes portfolio allocation ratios based on age and risk profile.
"""

from mock_agent import Agent
from pydantic import BaseModel
from typing import List, Dict, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Transaction, Fund, FundCategory, AgeGroup, RiskProfile


class OptimalAllocation(BaseModel):
    equity_ratio: float
    debt_ratio: float
    hybrid_ratio: float
    gold_silver_ratio: float


class RatioAnalysisResult(BaseModel):
    category: str = "ASSET_ALLOCATION"
    age_group: str
    risk_profile: str
    current_allocation: OptimalAllocation
    optimal_allocation: OptimalAllocation
    allocation_gap: OptimalAllocation
    recommendation: str
    rebalancing_required: bool
    action_required: bool


# Hardcoded optimal allocation matrix
OPTIMAL_ALLOCATIONS = {
    # Age group: {risk_profile: {equity, debt, hybrid, gold_silver}}
    AgeGroup.YOUNG_0_20: {
        RiskProfile.CONSERVATIVE: OptimalAllocation(equity_ratio=40.0, debt_ratio=40.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
        RiskProfile.MODERATE: OptimalAllocation(equity_ratio=60.0, debt_ratio=25.0, hybrid_ratio=10.0, gold_silver_ratio=5.0),
        RiskProfile.AGGRESSIVE: OptimalAllocation(equity_ratio=80.0, debt_ratio=10.0, hybrid_ratio=5.0, gold_silver_ratio=5.0),
    },
    AgeGroup.YOUNG_ADULT_20_30: {
        RiskProfile.CONSERVATIVE: OptimalAllocation(equity_ratio=50.0, debt_ratio=30.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
        RiskProfile.MODERATE: OptimalAllocation(equity_ratio=70.0, debt_ratio=15.0, hybrid_ratio=10.0, gold_silver_ratio=5.0),
        RiskProfile.AGGRESSIVE: OptimalAllocation(equity_ratio=85.0, debt_ratio=5.0, hybrid_ratio=5.0, gold_silver_ratio=5.0),
    },
    AgeGroup.ADULT_30_40: {
        RiskProfile.CONSERVATIVE: OptimalAllocation(equity_ratio=45.0, debt_ratio=35.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
        RiskProfile.MODERATE: OptimalAllocation(equity_ratio=65.0, debt_ratio=20.0, hybrid_ratio=10.0, gold_silver_ratio=5.0),
        RiskProfile.AGGRESSIVE: OptimalAllocation(equity_ratio=80.0, debt_ratio=10.0, hybrid_ratio=5.0, gold_silver_ratio=5.0),
    },
    AgeGroup.MIDDLE_AGE_40_50: {
        RiskProfile.CONSERVATIVE: OptimalAllocation(equity_ratio=35.0, debt_ratio=45.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
        RiskProfile.MODERATE: OptimalAllocation(equity_ratio=55.0, debt_ratio=30.0, hybrid_ratio=10.0, gold_silver_ratio=5.0),
        RiskProfile.AGGRESSIVE: OptimalAllocation(equity_ratio=70.0, debt_ratio=20.0, hybrid_ratio=5.0, gold_silver_ratio=5.0),
    },
    AgeGroup.PRE_RETIREMENT_50_60: {
        RiskProfile.CONSERVATIVE: OptimalAllocation(equity_ratio=25.0, debt_ratio=55.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
        RiskProfile.MODERATE: OptimalAllocation(equity_ratio=40.0, debt_ratio=40.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
        RiskProfile.AGGRESSIVE: OptimalAllocation(equity_ratio=55.0, debt_ratio=30.0, hybrid_ratio=10.0, gold_silver_ratio=5.0),
    },
    AgeGroup.SENIOR_60_PLUS: {
        RiskProfile.CONSERVATIVE: OptimalAllocation(equity_ratio=15.0, debt_ratio=65.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
        RiskProfile.MODERATE: OptimalAllocation(equity_ratio=25.0, debt_ratio=55.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
        RiskProfile.AGGRESSIVE: OptimalAllocation(equity_ratio=40.0, debt_ratio=40.0, hybrid_ratio=15.0, gold_silver_ratio=5.0),
    },
}


# Create the Ratio Analyzer agent
ratio_analyzer = Agent(
    'openai:gpt-4o-mini',
    result_type=RatioAnalysisResult,
    system_prompt="""
    You are an expert Portfolio Ratio Analyzer specializing in optimal asset allocation.
    
    Your responsibilities:
    1. Analyze current portfolio allocation across equity, debt, hybrid, and gold/silver
    2. Compare with optimal allocation based on age group and risk profile
    3. Identify allocation gaps and recommend rebalancing
    4. Provide specific action items for portfolio optimization
    
    Key principles:
    - Younger investors can take more equity risk
    - Conservative profiles prefer more debt allocation
    - Gold/silver serves as portfolio hedge (typically 5%)
    - Hybrid funds provide balanced exposure
    
    Always provide clear rebalancing recommendations with specific percentage targets.
    """,
)


def analyze_portfolio_ratios(
    transactions: List[Transaction], 
    funds: Dict[str, Fund], 
    age_group: AgeGroup, 
    risk_profile: RiskProfile
) -> RatioAnalysisResult:
    """
    Analyze portfolio allocation ratios against optimal targets.
    
    Args:
        transactions: All portfolio transactions
        funds: Fund details dictionary
        age_group: Investor's age group
        risk_profile: Investor's risk profile
        
    Returns:
        RatioAnalysisResult with allocation analysis and recommendations
    """
    # Calculate current allocation
    category_investments = {
        FundCategory.EQUITY: 0.0,
        FundCategory.DEBT: 0.0,
        FundCategory.HYBRID: 0.0,
        FundCategory.GOLD: 0.0,
        FundCategory.SILVER: 0.0,
    }
    
    # Group transactions by fund and calculate total investment per category
    for txn in transactions:
        if txn.transaction_type.value == "BUY":
            fund = funds.get(txn.fund_code)
            if fund:
                if fund.category in [FundCategory.GOLD, FundCategory.SILVER]:
                    # Combine gold and silver
                    category_investments[fund.category] += txn.transaction_count
                else:
                    category_investments[fund.category] += txn.transaction_count
    
    # Combine gold and silver
    gold_silver_total = category_investments[FundCategory.GOLD] + category_investments[FundCategory.SILVER]
    
    total_investment = sum(category_investments.values())
    
    if total_investment == 0:
        current_allocation = OptimalAllocation(
            equity_ratio=0.0,
            debt_ratio=0.0,
            hybrid_ratio=0.0,
            gold_silver_ratio=0.0
        )
    else:
        current_allocation = OptimalAllocation(
            equity_ratio=(category_investments[FundCategory.EQUITY] / total_investment) * 100,
            debt_ratio=(category_investments[FundCategory.DEBT] / total_investment) * 100,
            hybrid_ratio=(category_investments[FundCategory.HYBRID] / total_investment) * 100,
            gold_silver_ratio=(gold_silver_total / total_investment) * 100
        )
    
    # Get optimal allocation
    optimal_allocation = OPTIMAL_ALLOCATIONS[age_group][risk_profile]
    
    # Calculate allocation gaps
    allocation_gap = OptimalAllocation(
        equity_ratio=current_allocation.equity_ratio - optimal_allocation.equity_ratio,
        debt_ratio=current_allocation.debt_ratio - optimal_allocation.debt_ratio,
        hybrid_ratio=current_allocation.hybrid_ratio - optimal_allocation.hybrid_ratio,
        gold_silver_ratio=current_allocation.gold_silver_ratio - optimal_allocation.gold_silver_ratio
    )
    
    # Determine if rebalancing is needed (threshold: 10% deviation)
    rebalancing_threshold = 10.0
    rebalancing_required = any([
        abs(allocation_gap.equity_ratio) > rebalancing_threshold,
        abs(allocation_gap.debt_ratio) > rebalancing_threshold,
        abs(allocation_gap.hybrid_ratio) > rebalancing_threshold,
        abs(allocation_gap.gold_silver_ratio) > rebalancing_threshold
    ])
    
    # Prepare analysis context for LLM
    analysis_context = f"""
    Portfolio Allocation Analysis:
    
    Investor Profile:
    - Age Group: {age_group.value}
    - Risk Profile: {risk_profile.value}
    
    Current Allocation:
    - Equity: {current_allocation.equity_ratio:.1f}%
    - Debt: {current_allocation.debt_ratio:.1f}%
    - Hybrid: {current_allocation.hybrid_ratio:.1f}%
    - Gold/Silver: {current_allocation.gold_silver_ratio:.1f}%
    
    Optimal Allocation:
    - Equity: {optimal_allocation.equity_ratio:.1f}%
    - Debt: {optimal_allocation.debt_ratio:.1f}%
    - Hybrid: {optimal_allocation.hybrid_ratio:.1f}%
    - Gold/Silver: {optimal_allocation.gold_silver_ratio:.1f}%
    
    Allocation Gaps:
    - Equity: {allocation_gap.equity_ratio:+.1f}%
    - Debt: {allocation_gap.debt_ratio:+.1f}%
    - Hybrid: {allocation_gap.hybrid_ratio:+.1f}%
    - Gold/Silver: {allocation_gap.gold_silver_ratio:+.1f}%
    
    Total Portfolio Value: ₹{total_investment:,.2f}
    Rebalancing Required: {rebalancing_required}
    
    Please provide comprehensive allocation analysis with specific rebalancing recommendations.
    """
    
    # Call the LLM agent for analysis
    result = ratio_analyzer.run_sync(analysis_context)
    
    return RatioAnalysisResult(
        age_group=age_group.value,
        risk_profile=risk_profile.value,
        current_allocation=current_allocation,
        optimal_allocation=optimal_allocation,
        allocation_gap=allocation_gap,
        recommendation=result.data.recommendation,
        rebalancing_required=rebalancing_required,
        action_required=rebalancing_required
    )