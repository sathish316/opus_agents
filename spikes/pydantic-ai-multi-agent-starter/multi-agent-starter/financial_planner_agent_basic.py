import pandas as pd
import numpy_financial as npf
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import asyncio
from dataclasses import dataclass
from llm_helper import trace_all_messages
from pyxirr import xirr

@dataclass
class PortfolioAnalysis:
    """Portfolio of the customer. 
    Portfolio is a list of rows. Each row is a fund transaction record.
    Each row has the following fields:
    - Date: The date of the transaction
    - Fund Category: The category of the fund
    - Fund Code: The code of the fund
    - Fund Name: The name of the fund
    - Transaction Type: The type of transaction
    - Units: The number of units transacted
    - Unit Price: The price per unit at the time of transaction
    Portfolio details also contains the age bracket of the customer.
    """
    age_bracket: str = Field(..., description="The age bracket of the customer")
    fund_category: str = Field(..., description="The fund category to be analyzed")
    portfolio: list[dict] = Field(..., description="The portfolio of the customer. Portfolio is a list of rows."
                                  "Each row is a fund transaction record.")

def portfolio_to_dataframe(portfolio: PortfolioAnalysis) -> pd.DataFrame:
    """Convert a Portfolio object to a pandas DataFrame."""
    df = pd.DataFrame(portfolio.portfolio)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

# Planner agent that co-ordinates with the expert agents
financial_planner_agent = Agent(
    'openai:gpt-4o',
    deps_type=PortfolioAnalysis,
    output_type=str,
    system_prompt=(
        'Use the tool `analyze_fund_category` to perform analysis on the portfolio for a given fund category. Fund category values are EQ for Equity, DT for Debt, HY for Hybrid.'
        'This tool will return xirr for a fund category.'
    ),
)

# Tool to link planner agent with sub-agents
@financial_planner_agent.tool
async def analyze_fund_category(ctx: RunContext[PortfolioAnalysis], fund_category: str) -> str:
    xirr = calculate_xirr_for_fund_category(ctx.deps, fund_category)
    xirr_result = f"XIRR for {fund_category} is {xirr}"
    return xirr_result
        
# Util functions which are indirectly used by the tools
def calculate_xirr_for_fund_category(portfolio: PortfolioAnalysis, fund_category: str) -> float:
    """Calculate XIRR of Fund category. Fund category values are EQ, DT, HY"""
    portfolio_df = portfolio_to_dataframe(portfolio)
    fund_category_df = portfolio_df[portfolio_df['fund_category'] == fund_category]
    print("Calculating XIRR...")
    print(fund_category_df.head())
    return calculate_xirr(fund_category_df)

def calculate_xirr(transactions: pd.DataFrame) -> float:
    """Calculates the XIRR for a series of transactions."""
    values = []
    dates = []
    for _, row in transactions.iterrows():
        values.append(-row['units'] * row['unit_price'])
        dates.append(row['Date'])

    # Add the current value of the investment
    current_price = transactions['unit_price'].iloc[-1]
    total_units = transactions['units'].sum()
    values.append(total_units * current_price)
    dates.append(datetime.now())
    # print("Values for XIRR:")
    # for i, (value, date) in enumerate(zip(values, dates)):
        # print(f"{date}\t{value}")
    try:
        result = xirr(dates, values)
        return result
    except Exception as e:
        print(f"XIRR calculation failed: {e}")
        return 0.0

# util functions
def load_portfolio(filepath: str) -> pd.DataFrame:
    """Loads the portfolio from a CSV file."""
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

async def main():
    """Main function to run the portfolio planner."""
    # Load the portfolio
    portfolio_df = load_portfolio("./data/portfolio.csv")
    print(portfolio_df.head())
    deps = PortfolioAnalysis(
        portfolio=portfolio_df.to_dict(orient='records'), 
        age_bracket="30-40", 
        fund_category='EQ'
    )

    result = await financial_planner_agent.run(
        f"""Analyze my portfolio and calculate XIRR for Equity funds:
        Portfolio:
        {deps.portfolio}
        
        Age group:
        {deps.age_bracket}
        
        Analysis for fund category:
        {deps.fund_category}
        """,
        deps = deps
    )
    print(result.output)
    print(result.usage())
    trace_all_messages(result)

if __name__ == "__main__":
    asyncio.run(main())