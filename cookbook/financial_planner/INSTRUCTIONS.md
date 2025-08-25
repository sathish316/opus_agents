# Using the Financial Planner with Real PydanticAI

This document explains how to convert the demo system to use actual PydanticAI agents instead of the mock implementation.

## Quick Start with Real PydanticAI

### 1. Install PydanticAI

```bash
pip install pydantic-ai[openai]
```

### 2. Set Environment Variables

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Replace Mock Agent Import

In each agent file, change:

```python
# FROM:
from mock_agent import Agent

# TO:
from pydantic_ai import Agent
```

Files to update:
- `agents/equity_fund_manager.py`
- `agents/debt_fund_manager.py`
- `agents/hybrid_fund_manager.py`
- `agents/gold_silver_fund_manager.py`
- `agents/ratio_analyzer.py`
- `portfolio_analyzer.py`

### 4. Update Requirements

```bash
# Remove or comment out mock-specific dependencies
# Add to requirements.txt:
pydantic-ai[openai]>=0.0.14
```

## Agent Configuration Examples

### Real PydanticAI Agent Setup

```python
from pydantic_ai import Agent

# Equity Fund Manager with real LLM
equity_fund_manager = Agent(
    'openai:gpt-4o-mini',  # or 'openai:gpt-4'
    result_type=EquityAnalysisResult,
    system_prompt="""
    You are an expert Equity Fund Manager specializing in Indian mutual funds.
    
    Your responsibilities:
    1. Filter and analyze only equity-based funds from the portfolio
    2. Calculate XIRR for equity investments
    3. Compare performance against benchmark (12% for equity)
    4. Recommend marquee index funds if performance is below optimal
    5. Provide clear, actionable recommendations
    
    Key metrics for equity funds in India:
    - Expected minimum XIRR: 12%
    - Recommended marquee funds: UTI Nifty Index, SBI Sensex Index, HDFC Nifty 50
    
    Always provide specific, data-driven recommendations with clear reasoning.
    """,
)
```

### Using Different LLM Models

```python
# OpenAI GPT-4
Agent('openai:gpt-4', ...)

# OpenAI GPT-3.5 Turbo
Agent('openai:gpt-3.5-turbo', ...)

# Anthropic Claude
Agent('anthropic:claude-3-sonnet-20240229', ...)

# Google Gemini
Agent('gemini:gemini-pro', ...)
```

## Real-world Integration Options

### 1. Live NAV Data Integration

Replace mock NAV data with real APIs:

```python
import yfinance as yf
import requests

def get_real_fund_nav(fund_code: str) -> float:
    """Get real NAV from fund house APIs or financial data providers."""
    # Example with Indian mutual fund APIs
    url = f"https://api.mfapi.in/mf/{fund_code}"
    response = requests.get(url)
    data = response.json()
    return float(data['data'][0]['nav'])

def get_stock_price(symbol: str) -> float:
    """Get stock price for index tracking."""
    ticker = yf.Ticker(f"{symbol}.NS")  # NSE suffix for Indian stocks
    hist = ticker.history(period="1d")
    return hist['Close'].iloc[-1]
```

### 2. Enhanced Analytics

Add advanced financial calculations:

```python
import numpy as np
from scipy.stats import norm

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.05) -> float:
    """Calculate Sharpe ratio for risk-adjusted returns."""
    excess_returns = np.array(returns) - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns)

def calculate_var(returns: List[float], confidence_level: float = 0.05) -> float:
    """Calculate Value at Risk."""
    return np.percentile(returns, confidence_level * 100)

def monte_carlo_simulation(initial_value: float, mean_return: float, 
                          volatility: float, years: int, simulations: int = 1000) -> List[float]:
    """Run Monte Carlo simulation for portfolio projections."""
    results = []
    for _ in range(simulations):
        value = initial_value
        for _ in range(years * 252):  # Daily simulation
            daily_return = np.random.normal(mean_return/252, volatility/np.sqrt(252))
            value *= (1 + daily_return)
        results.append(value)
    return results
```

### 3. Goal-Based Planning

Add specific financial goals:

```python
class FinancialGoal(BaseModel):
    name: str
    target_amount: float
    target_date: datetime
    priority: int
    risk_tolerance: RiskProfile

class GoalPlannerAgent:
    """Agent for goal-based financial planning."""
    
    def calculate_sip_amount(self, goal: FinancialGoal, expected_return: float) -> float:
        """Calculate required SIP amount for goal achievement."""
        months = (goal.target_date.year - datetime.now().year) * 12
        monthly_rate = expected_return / 12 / 100
        
        # SIP formula: FV = PMT * [((1 + r)^n - 1) / r]
        pmt = goal.target_amount / (((1 + monthly_rate) ** months - 1) / monthly_rate)
        return pmt
```

### 4. Tax Optimization

Add tax-aware recommendations:

```python
class TaxOptimizer:
    """Optimize portfolio for tax efficiency."""
    
    def calculate_ltcg_tax(self, gains: float) -> float:
        """Calculate Long Term Capital Gains tax in India."""
        exemption = 100000  # ₹1 lakh exemption for equity
        taxable_gains = max(0, gains - exemption)
        return taxable_gains * 0.10  # 10% LTCG tax
    
    def suggest_tax_loss_harvesting(self, portfolio: List[Fund]) -> List[str]:
        """Suggest funds for tax loss harvesting."""
        recommendations = []
        for fund in portfolio:
            if fund.current_value < fund.invested_amount:
                loss_amount = fund.invested_amount - fund.current_value
                recommendations.append(
                    f"Consider booking loss in {fund.name}: ₹{loss_amount:,.2f}"
                )
        return recommendations
```

## Production Deployment

### 1. API Service

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Portfolio Analysis API")

class AnalysisRequest(BaseModel):
    portfolio_data: List[Transaction]
    age_group: AgeGroup
    risk_profile: RiskProfile

@app.post("/analyze")
async def analyze_portfolio(request: AnalysisRequest):
    analyzer = PortfolioAnalyzer()
    analyzer.transactions = request.portfolio_data
    
    result = analyzer.analyze_portfolio(
        age_group=request.age_group,
        risk_profile=request.risk_profile
    )
    
    return result
```

### 2. Scheduled Analysis

```python
import schedule
import time

def daily_portfolio_update():
    """Run daily portfolio analysis for all users."""
    analyzer = PortfolioAnalyzer()
    # Load user portfolios from database
    # Run analysis and send alerts/reports
    pass

schedule.every().day.at("09:00").do(daily_portfolio_update)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. Database Integration

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    fund_code = Column(String)
    fund_name = Column(String)
    transaction_type = Column(String)
    transaction_count = Column(Float)
    transaction_date = Column(DateTime)
    created_at = Column(DateTime)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    analysis_date = Column(DateTime)
    total_investment = Column(Float)
    current_value = Column(Float)
    overall_xirr = Column(Float)
    risk_score = Column(Float)
    recommendations = Column(String)  # JSON string
```

## Testing Strategy

### 1. Unit Tests

```python
import pytest
from portfolio_analyzer import PortfolioAnalyzer

def test_xirr_calculation():
    """Test XIRR calculation accuracy."""
    transactions = create_test_transactions()
    xirr = calculate_xirr(transactions, current_nav=110.0)
    assert 8.0 <= xirr <= 15.0  # Reasonable range

def test_agent_communication():
    """Test agent coordination."""
    analyzer = PortfolioAnalyzer()
    analyzer.load_test_data()
    result = analyzer.analyze_portfolio()
    assert result.overall_xirr is not None
    assert len(result.action_items) >= 0
```

### 2. Integration Tests

```python
def test_end_to_end_analysis():
    """Test complete analysis workflow."""
    analyzer = PortfolioAnalyzer()
    analyzer.load_portfolio('test_portfolio.csv')
    
    result = analyzer.analyze_portfolio(
        age_group=AgeGroup.ADULT_30_40,
        risk_profile=RiskProfile.MODERATE
    )
    
    assert result.total_investment > 0
    assert result.risk_score >= 0
    assert len(result.recommendations) > 0
```

## Monitoring and Alerts

### 1. Performance Monitoring

```python
import logging
from datetime import datetime

def monitor_portfolio_performance():
    """Monitor and alert on significant portfolio changes."""
    analyzer = PortfolioAnalyzer()
    current_analysis = analyzer.analyze_portfolio()
    
    # Check for significant changes
    if current_analysis.risk_score > 70:
        send_alert(f"High risk detected: {current_analysis.risk_score}")
    
    if current_analysis.overall_xirr < -10:
        send_alert(f"Significant losses: {current_analysis.overall_xirr}%")

def send_alert(message: str):
    """Send alert via email/SMS/Slack."""
    logging.warning(f"Portfolio Alert: {message}")
    # Implement notification logic
```

This completes the comprehensive financial planner system with detailed instructions for real-world deployment!