#!/usr/bin/env python3
"""
Financial Planner Demo Script

This script demonstrates the comprehensive portfolio analysis system with multiple
PydanticAI agents working together to analyze mutual fund portfolios.
"""

import sys
import os
from portfolio_analyzer import PortfolioAnalyzer
from models import AgeGroup, RiskProfile

def print_separator(title=""):
    """Print a formatted separator."""
    print("\n" + "="*80)
    if title:
        print(f" {title}")
        print("="*80)

def demo_portfolio_analysis():
    """Demonstrate the complete portfolio analysis workflow."""
    
    print_separator("FINANCIAL PLANNER MULTI-AGENT DEMO")
    print("This demo shows how multiple PydanticAI agents work together")
    print("to analyze a mutual fund portfolio and provide recommendations.")
    
    # Initialize the portfolio analyzer
    print_separator("STEP 1: LOADING PORTFOLIO DATA")
    analyzer = PortfolioAnalyzer()
    
    try:
        analyzer.load_portfolio('portfolio.csv')
        print("✓ Portfolio loaded successfully from portfolio.csv")
        print(f"✓ Found {len(analyzer.transactions)} transactions")
        print(f"✓ Analyzing {len(analyzer.funds)} unique funds")
        
        # Display fund summary
        print("\nFunds in Portfolio:")
        for fund_code, fund in analyzer.funds.items():
            print(f"  • {fund.name} ({fund.category.value})")
            
    except Exception as e:
        print(f"✗ Error loading portfolio: {e}")
        return
    
    # Analyze for different investor profiles
    profiles = [
        (AgeGroup.YOUNG_ADULT_20_30, RiskProfile.AGGRESSIVE, "25-year-old Aggressive Investor"),
        (AgeGroup.ADULT_30_40, RiskProfile.MODERATE, "35-year-old Moderate Investor"),
        (AgeGroup.PRE_RETIREMENT_50_60, RiskProfile.CONSERVATIVE, "55-year-old Conservative Investor"),
    ]
    
    for age_group, risk_profile, description in profiles:
        print_separator(f"ANALYSIS FOR: {description}")
        
        try:
            summary = analyzer.analyze_portfolio(
                age_group=age_group,
                risk_profile=risk_profile
            )
            
            # Display key metrics
            print(f"📊 PORTFOLIO OVERVIEW")
            print(f"   Total Investment: ₹{summary.total_investment:,.2f}")
            print(f"   Current Value: ₹{summary.current_value:,.2f}")
            print(f"   Overall XIRR: {summary.overall_xirr:.2f}%")
            print(f"   Risk Score: {summary.risk_score:.0f}/100")
            
            gains_losses = summary.current_value - summary.total_investment
            gains_pct = (gains_losses / summary.total_investment * 100) if summary.total_investment > 0 else 0
            status = "📈 Gains" if gains_losses >= 0 else "📉 Losses"
            print(f"   {status}: ₹{gains_losses:,.2f} ({gains_pct:+.2f}%)")
            
            # Display risk assessment
            if summary.risk_score <= 20:
                risk_level = "🟢 LOW RISK"
            elif summary.risk_score <= 50:
                risk_level = "🟡 MODERATE RISK"
            else:
                risk_level = "🔴 HIGH RISK"
            print(f"   Risk Level: {risk_level}")
            
            # Display agent-specific analysis
            print(f"\n🤖 AGENT ANALYSIS SUMMARY")
            print(f"   Equity Funds: {summary.equity_analysis[:100]}...")
            print(f"   Debt Funds: {summary.debt_analysis[:100]}...")
            print(f"   Hybrid Funds: {summary.hybrid_analysis[:100]}...")
            print(f"   Gold/Silver: {summary.gold_silver_analysis[:100]}...")
            print(f"   Allocation: {summary.allocation_analysis[:100]}...")
            
            # Display recommendations
            print(f"\n💡 KEY RECOMMENDATIONS")
            print(f"   {summary.overall_recommendation}")
            
            if summary.action_items:
                print(f"\n📋 ACTION ITEMS ({len(summary.action_items)})")
                for i, action in enumerate(summary.action_items, 1):
                    print(f"   {i}. {action}")
            else:
                print(f"\n✅ No immediate actions required!")
                
        except Exception as e:
            print(f"✗ Error analyzing portfolio: {e}")
    
    print_separator("AGENT ARCHITECTURE OVERVIEW")
    print("The system uses 6 specialized PydanticAI agents:")
    print("")
    print("1. 🏢 EquityFundManager")
    print("   - Analyzes equity fund performance")
    print("   - Compares against 12% benchmark")
    print("   - Recommends marquee index funds")
    print("")
    print("2. 🏦 DebtFundManager") 
    print("   - Analyzes debt fund performance")
    print("   - Compares against 7.5% benchmark")
    print("   - Focuses on capital preservation")
    print("")
    print("3. ⚖️  HybridFundManager")
    print("   - Analyzes balanced fund performance")
    print("   - Compares against 10% benchmark")
    print("   - Balances growth and stability")
    print("")
    print("4. 🥇 GoldSilverFundManager")
    print("   - Analyzes precious metals exposure")
    print("   - Maintains 50:50 gold-silver ratio")
    print("   - Provides inflation hedging")
    print("")
    print("5. 📊 RatioAnalyzer")
    print("   - Optimizes asset allocation")
    print("   - Considers age and risk profile")
    print("   - 18 allocation combinations")
    print("")
    print("6. 🎯 PortfolioAnalyzer (Main Coordinator)")
    print("   - Orchestrates all sub-agents")
    print("   - Provides comprehensive analysis")
    print("   - Generates actionable insights")
    
    print_separator("TECHNICAL FEATURES")
    print("✓ XIRR calculation for each fund category")
    print("✓ Benchmark comparison and performance analysis")
    print("✓ Age-based asset allocation optimization")
    print("✓ Risk profiling (Conservative/Moderate/Aggressive)")
    print("✓ Multi-agent communication and coordination")
    print("✓ Structured data models with Pydantic")
    print("✓ Comprehensive recommendation engine")
    print("✓ Mock LLM integration (ready for real LLM)")
    print("✓ Extensible architecture for new fund types")
    
    print_separator("DEMO COMPLETED")
    print("The Financial Planner demonstrates how to build sophisticated")
    print("multi-agent systems with PydanticAI for real-world applications.")
    print("\nTo use with real LLM:")
    print("1. Replace mock_agent.py with actual PydanticAI")
    print("2. Set OPENAI_API_KEY environment variable")
    print("3. Install: pip install pydantic-ai")


if __name__ == "__main__":
    demo_portfolio_analysis()