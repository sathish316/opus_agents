# Financial Planner with PydanticAI Agents

A comprehensive portfolio analysis system built with PydanticAI that uses multiple specialized agents to analyze mutual fund portfolios and provide investment recommendations.

## Overview

This system demonstrates how to build a multi-agent financial analysis platform using PydanticAI. It includes specialized agents for different fund categories and provides comprehensive portfolio analysis with actionable recommendations.

## Architecture

### Main Components

1. **PortfolioAnalyzer**: Main coordinator agent that orchestrates all sub-agents
2. **Specialized Fund Managers**:
   - **EquityFundManager**: Analyzes equity-based funds
   - **DebtFundManager**: Analyzes debt-based funds  
   - **HybridFundManager**: Analyzes hybrid/balanced funds
   - **GoldSilverFundManager**: Analyzes precious metals funds
3. **RatioAnalyzer**: Analyzes asset allocation based on age and risk profile

### Agent Communication

Agents communicate through:
- Structured data models (Pydantic BaseModel)
- Shared utility functions for calculations
- Centralized data loading and processing
- Results aggregation in the main analyzer

## Features

### Fund Analysis
- **XIRR Calculation**: Calculates Extended Internal Rate of Return for each fund category
- **Benchmark Comparison**: Compares performance against category benchmarks
- **Recommendation Engine**: Suggests marquee funds when performance is below optimal

### Asset Allocation
- **Age-based Allocation**: Optimal ratios based on 6 age groups (0-20, 20-30, 30-40, 40-50, 50-60, 60+)
- **Risk Profile Integration**: Conservative, Moderate, Aggressive risk profiles
- **Rebalancing Recommendations**: Specific suggestions for portfolio rebalancing

### Performance Metrics
- Portfolio-wide XIRR calculation
- Risk assessment (0-100 scale)
- Action items prioritization
- Comprehensive reporting

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key (required for LLM analysis)
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Basic Portfolio Analysis

```python
from portfolio_analyzer import PortfolioAnalyzer
from models import AgeGroup, RiskProfile

# Initialize analyzer
analyzer = PortfolioAnalyzer()

# Load portfolio from CSV
analyzer.load_portfolio('portfolio.csv')

# Analyze for 35-year-old moderate risk investor
summary = analyzer.analyze_portfolio(
    age_group=AgeGroup.ADULT_30_40,
    risk_profile=RiskProfile.MODERATE
)

# View results
print(f"Total Investment: ₹{summary.total_investment:,.2f}")
print(f"Overall XIRR: {summary.overall_xirr:.2f}%")
print(f"Risk Score: {summary.risk_score}/100")
print(summary.overall_recommendation)
```

### Portfolio CSV Format

```csv
date,fund_code,fund_name,transaction_type,transaction_count
2023-01-15,UTI_NIFTY,UTI Nifty Index Fund,BUY,5000
2023-02-15,UTI_NIFTY,UTI Nifty Index Fund,BUY,5000
...
```

### Running the Example

```bash
cd /workspace/cookbook/financial_planner
python portfolio_analyzer.py
```

## Agent Specifications

### EquityFundManager
- **Benchmark XIRR**: 12%
- **Recommended Funds**: UTI Nifty Index, SBI Sensex Index, HDFC Nifty 50
- **Focus**: Growth and long-term wealth creation

### DebtFundManager  
- **Benchmark XIRR**: 7.5%
- **Recommended Funds**: SBI Magnum Gilt, HDFC Short Term Debt, ICICI Liquid Fund
- **Focus**: Capital preservation and steady income

### HybridFundManager
- **Benchmark XIRR**: 10%
- **Recommended Funds**: HDFC Balanced Advantage, ICICI Balanced Advantage, SBI Balanced Advantage
- **Focus**: Balanced growth with managed volatility

### GoldSilverFundManager
- **Benchmark XIRR**: 8% (Gold), 9% (Silver)
- **Recommended Allocation**: 50:50 Gold-Silver ratio
- **Recommended Funds**: Nippon Gold Savings, HDFC Gold, Kotak Silver ETF
- **Focus**: Portfolio hedging and inflation protection

### RatioAnalyzer
- **Allocation Matrix**: 18 combinations (6 age groups × 3 risk profiles)
- **Rebalancing Threshold**: 10% deviation from optimal
- **Focus**: Age-appropriate asset allocation optimization

## Optimal Allocation Examples

| Age Group | Risk Profile | Equity | Debt | Hybrid | Gold/Silver |
|-----------|--------------|--------|------|--------|-------------|
| 20-30     | Aggressive   | 85%    | 5%   | 5%     | 5%          |
| 30-40     | Moderate     | 65%    | 20%  | 10%    | 5%          |
| 50-60     | Conservative | 25%    | 55%  | 15%    | 5%          |

## Extensions

This system can be easily extended with:

1. **Additional Asset Classes**: REITs, International funds, Sectoral funds
2. **Advanced Analytics**: Sharpe ratio, Alpha/Beta calculations, Monte Carlo simulations
3. **Real-time Data**: Integration with live NAV APIs
4. **Tax Optimization**: Tax-loss harvesting, LTCG planning
5. **Goal-based Planning**: SIP calculators, retirement planning
6. **Risk Management**: Stop-loss mechanisms, volatility analysis

## Testing

The system includes a sample `portfolio.csv` with:
- 2 equity index funds (12 SIPs each)
- 1 debt fund (4 SIPs)
- 1 hybrid fund (4 SIPs) 
- 1 gold fund (4 SIPs)

Total portfolio value: ₹66,000 across 24 transactions

## Architecture Benefits

1. **Modularity**: Each agent handles specific fund categories
2. **Scalability**: Easy to add new fund types or analysis methods
3. **Maintainability**: Clear separation of concerns
4. **Extensibility**: Simple to integrate with external APIs
5. **Testability**: Individual agents can be tested independently

This example demonstrates building sophisticated multi-agent systems with PydanticAI for real-world financial analysis applications.