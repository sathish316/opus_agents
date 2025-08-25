"""
Main Portfolio Analyzer Agent - Coordinates all sub-agents for comprehensive portfolio analysis.
"""

from mock_agent import Agent
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

from models import Transaction, Fund, PortfolioAnalysis, AgeGroup, RiskProfile
from utils import load_portfolio_from_csv
from agents.equity_fund_manager import analyze_equity_portfolio
from agents.debt_fund_manager import analyze_debt_portfolio
from agents.hybrid_fund_manager import analyze_hybrid_portfolio
from agents.gold_silver_fund_manager import analyze_gold_silver_portfolio
from agents.ratio_analyzer import analyze_portfolio_ratios


class PortfolioSummary(BaseModel):
    total_investment: float
    current_value: float
    overall_xirr: float
    equity_analysis: str
    debt_analysis: str
    hybrid_analysis: str
    gold_silver_analysis: str
    allocation_analysis: str
    overall_recommendation: str
    risk_score: float
    action_items: List[str]


# Create the main Portfolio Analyzer agent
portfolio_analyzer = Agent(
    'openai:gpt-4o-mini',
    result_type=PortfolioSummary,
    system_prompt="""
    You are a comprehensive Portfolio Analyzer coordinating multiple specialized fund managers.
    
    Your responsibilities:
    1. Synthesize analysis from all specialized agents (Equity, Debt, Hybrid, Gold/Silver, Ratio)
    2. Provide overall portfolio assessment and recommendations
    3. Calculate risk scores and identify priority action items
    4. Deliver clear, actionable insights for portfolio optimization
    
    Consider:
    - Performance across all asset classes
    - Asset allocation optimization
    - Risk-adjusted returns
    - Age and risk profile appropriateness
    - Market conditions and diversification
    
    Provide specific, prioritized recommendations with clear reasoning.
    """,
)


class PortfolioAnalyzer:
    """
    Main portfolio analyzer that coordinates all sub-agents.
    """
    
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.funds: Dict[str, Fund] = {}
    
    def load_portfolio(self, csv_file_path: str) -> None:
        """Load portfolio data from CSV file."""
        self.transactions, self.funds = load_portfolio_from_csv(csv_file_path)
    
    def analyze_portfolio(
        self, 
        age_group: AgeGroup = AgeGroup.ADULT_30_40,
        risk_profile: RiskProfile = RiskProfile.MODERATE
    ) -> PortfolioSummary:
        """
        Perform comprehensive portfolio analysis using all sub-agents.
        
        Args:
            age_group: Investor's age group
            risk_profile: Investor's risk profile
            
        Returns:
            PortfolioSummary with comprehensive analysis
        """
        if not self.transactions:
            raise ValueError("No portfolio data loaded. Please load portfolio CSV first.")
        
        # Analyze each category using specialized agents
        equity_result = analyze_equity_portfolio(self.transactions, self.funds)
        debt_result = analyze_debt_portfolio(self.transactions, self.funds)
        hybrid_result = analyze_hybrid_portfolio(self.transactions, self.funds)
        gold_silver_result = analyze_gold_silver_portfolio(self.transactions, self.funds)
        ratio_result = analyze_portfolio_ratios(self.transactions, self.funds, age_group, risk_profile)
        
        # Calculate overall metrics
        total_investment = (equity_result.total_invested + 
                          debt_result.total_invested + 
                          hybrid_result.total_invested + 
                          gold_silver_result.total_invested)
        
        current_value = (equity_result.current_value + 
                        debt_result.current_value + 
                        hybrid_result.current_value + 
                        gold_silver_result.current_value)
        
        # Calculate weighted average XIRR
        if total_investment > 0:
            overall_xirr = (
                (equity_result.portfolio_xirr * equity_result.total_invested +
                 debt_result.portfolio_xirr * debt_result.total_invested +
                 hybrid_result.portfolio_xirr * hybrid_result.total_invested +
                 gold_silver_result.portfolio_xirr * gold_silver_result.total_invested) 
                / total_investment
            )
        else:
            overall_xirr = 0.0
        
        # Calculate risk score (0-100, lower is better)
        risk_factors = []
        if equity_result.action_required:
            risk_factors.append(20)
        if debt_result.action_required:
            risk_factors.append(15)
        if hybrid_result.action_required:
            risk_factors.append(10)
        if gold_silver_result.action_required:
            risk_factors.append(10)
        if ratio_result.action_required:
            risk_factors.append(25)
        
        risk_score = sum(risk_factors)
        
        # Compile action items
        action_items = []
        if equity_result.action_required:
            action_items.append(f"Equity: {equity_result.recommendation[:100]}...")
        if debt_result.action_required:
            action_items.append(f"Debt: {debt_result.recommendation[:100]}...")
        if hybrid_result.action_required:
            action_items.append(f"Hybrid: {hybrid_result.recommendation[:100]}...")
        if gold_silver_result.action_required:
            action_items.append(f"Gold/Silver: {gold_silver_result.recommendation[:100]}...")
        if ratio_result.action_required:
            action_items.append(f"Allocation: {ratio_result.recommendation[:100]}...")
        
        # Prepare comprehensive analysis for LLM
        analysis_context = f"""
        Comprehensive Portfolio Analysis Summary:
        
        Overall Portfolio Metrics:
        - Total Investment: ₹{total_investment:,.2f}
        - Current Value: ₹{current_value:,.2f}
        - Overall XIRR: {overall_xirr:.2f}%
        - Risk Score: {risk_score}/100
        - Investor Profile: {age_group.value}, {risk_profile.value}
        
        Asset Class Performance:
        
        1. EQUITY ({equity_result.funds_analyzed} funds):
           - Invested: ₹{equity_result.total_invested:,.2f}
           - XIRR: {equity_result.portfolio_xirr:.2f}% (Benchmark: {equity_result.benchmark_xirr:.2f}%)
           - Action Required: {equity_result.action_required}
        
        2. DEBT ({debt_result.funds_analyzed} funds):
           - Invested: ₹{debt_result.total_invested:,.2f}
           - XIRR: {debt_result.portfolio_xirr:.2f}% (Benchmark: {debt_result.benchmark_xirr:.2f}%)
           - Action Required: {debt_result.action_required}
        
        3. HYBRID ({hybrid_result.funds_analyzed} funds):
           - Invested: ₹{hybrid_result.total_invested:,.2f}
           - XIRR: {hybrid_result.portfolio_xirr:.2f}% (Benchmark: {hybrid_result.benchmark_xirr:.2f}%)
           - Action Required: {hybrid_result.action_required}
        
        4. GOLD/SILVER ({gold_silver_result.funds_analyzed} funds):
           - Invested: ₹{gold_silver_result.total_invested:,.2f}
           - XIRR: {gold_silver_result.portfolio_xirr:.2f}% (Benchmark: {gold_silver_result.benchmark_xirr:.2f}%)
           - Gold Allocation: {gold_silver_result.gold_allocation:.1f}%
           - Silver Allocation: {gold_silver_result.silver_allocation:.1f}%
           - Action Required: {gold_silver_result.action_required}
        
        5. ASSET ALLOCATION:
           - Current vs Optimal Equity: {ratio_result.current_allocation.equity_ratio:.1f}% vs {ratio_result.optimal_allocation.equity_ratio:.1f}%
           - Current vs Optimal Debt: {ratio_result.current_allocation.debt_ratio:.1f}% vs {ratio_result.optimal_allocation.debt_ratio:.1f}%
           - Current vs Optimal Hybrid: {ratio_result.current_allocation.hybrid_ratio:.1f}% vs {ratio_result.optimal_allocation.hybrid_ratio:.1f}%
           - Current vs Optimal Gold/Silver: {ratio_result.current_allocation.gold_silver_ratio:.1f}% vs {ratio_result.optimal_allocation.gold_silver_ratio:.1f}%
           - Rebalancing Required: {ratio_result.rebalancing_required}
        
        Individual Agent Recommendations:
        - Equity: {equity_result.recommendation}
        - Debt: {debt_result.recommendation}
        - Hybrid: {hybrid_result.recommendation}
        - Gold/Silver: {gold_silver_result.recommendation}
        - Allocation: {ratio_result.recommendation}
        
        Please provide a comprehensive portfolio summary with prioritized recommendations.
        """
        
        # Get LLM analysis
        result = portfolio_analyzer.run_sync(analysis_context)
        
        return PortfolioSummary(
            total_investment=total_investment,
            current_value=current_value,
            overall_xirr=overall_xirr,
            equity_analysis=equity_result.recommendation,
            debt_analysis=debt_result.recommendation,
            hybrid_analysis=hybrid_result.recommendation,
            gold_silver_analysis=gold_silver_result.recommendation,
            allocation_analysis=ratio_result.recommendation,
            overall_recommendation=result.data.overall_recommendation,
            risk_score=risk_score,
            action_items=action_items
        )


def main():
    """Example usage of the Portfolio Analyzer."""
    analyzer = PortfolioAnalyzer()
    
    # Load portfolio
    analyzer.load_portfolio('/workspace/cookbook/financial_planner/portfolio.csv')
    
    # Analyze for a 35-year-old moderate risk investor
    summary = analyzer.analyze_portfolio(
        age_group=AgeGroup.ADULT_30_40,
        risk_profile=RiskProfile.MODERATE
    )
    
    # Print results
    print("=== PORTFOLIO ANALYSIS SUMMARY ===")
    print(f"Total Investment: ₹{summary.total_investment:,.2f}")
    print(f"Current Value: ₹{summary.current_value:,.2f}")
    print(f"Overall XIRR: {summary.overall_xirr:.2f}%")
    print(f"Risk Score: {summary.risk_score}/100")
    print(f"\nOverall Recommendation:\n{summary.overall_recommendation}")
    
    print(f"\n=== ACTION ITEMS ===")
    for i, action in enumerate(summary.action_items, 1):
        print(f"{i}. {action}")


if __name__ == "__main__":
    main()