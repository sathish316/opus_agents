import pandas as pd
import numpy_financial as npf
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import asyncio
from dataclasses import dataclass
from llm_helper import trace_all_messages
from pyxirr import xirr
from typing import Annotated, TypedDict, NotRequired
import logging
    
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FundTransaction(TypedDict):
    date: NotRequired[Annotated[datetime, Field(description="The date of the transaction")]]
    fund_category: Annotated[str, Field(description="The category of the fund (EQ for Equity, DT for Debt, HY for Hybrid)")]
    fund_code: Annotated[str, Field(description="The unique code identifier of the fund")]
    fund_name: Annotated[str, Field(description="The name of the fund")]
    transaction_type: Annotated[str, Field(description="The type of transaction (buy, sell, etc.)")]
    units: Annotated[float, Field(description="The number of units transacted")]
    unit_price: Annotated[float, Field(description="The price per unit at the time of transaction")]

class PortfolioAnalysis(BaseModel):
    """
    Portfolio Analysis for a customer. 
    Portfolio is a list of rows. Each row is a FundTransaction object.
    """
    portfolio: list[FundTransaction] = Field(..., description="The portfolio of the customer. Portfolio is a list of FundTransaction records.")
    age_range: str = Field(..., description="The age range of the customer")

# Util functions
def portfolio_to_dataframe(portfolio: PortfolioAnalysis) -> pd.DataFrame:
    """Convert a Portfolio object to a pandas DataFrame."""
    df = pd.DataFrame(portfolio.portfolio)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

# Planner agent that co-ordinates with the expert agents
financial_planner_agent = Agent(
    'claude-sonnet-4-20250514',
    deps_type=PortfolioAnalysis,
    output_type=str,
    system_prompt=(
        'You are a Financial Planner.'
        'You are given the portfolio of a customer for analysis.'
        'You are also given customer profile details like age range.'
        'You have a team of Expert agents for analysis of each fund category - Equity(EQ), Debt(DT), Hybrid(HY).'
        'Use the tool `analyze_fund_category` to perform analysis on the portfolio across fund categories like Equity(EQ), Debt(DT), Hybrid(HY).'
        'This tool will return XIRR for all funds in a fund category and a recommended fund if the XIRR of current funds is not optimal.'
        'You have an Expert agent for Asset Allocation.' 
        'Use the tool `analyze_asset_allocation` to perform Asset allocation ratio analysis on the portfolio, given a customer profile like age range.'
        'This tool will return a recommendation for rebalancing the portfolio if required.'
        'Your job is to use the tools to perform analysis on the portfolio and provide a Financial report with recommendations.'
    ),
)

# Tool to link planner agent with sub-agents
@financial_planner_agent.tool
async def analyze_fund_category(ctx: RunContext[PortfolioAnalysis], fund_category: str) -> str:
    if fund_category == 'EQ':
        response = await equity_fund_agent.run(
            "Analyze the portfolio for Equity funds",
            deps=ctx.deps
        )
        return response.output
    elif fund_category == 'DT':
        response = await debt_fund_agent.run(
            "Analyze the portfolio for Debt funds",
            deps=ctx.deps
        )
        return response.output
    elif fund_category == 'HY':
        response = await hybrid_fund_agent.run(
            "Analyze the portfolio for Hybrid funds",
            deps=ctx.deps
        )
        return response.output
    else:
        return 'Invalid fund category'

# Another Tool to link planner agent with sub-agent
@financial_planner_agent.tool
async def analyze_asset_allocation(ctx: RunContext[PortfolioAnalysis]) -> str:
    """Analyze the portfolio for optimal Asset Allocation based on the customer's age range"""
    result = await asset_allocation_agent.run(
        "Analyze the portfolio for optimal Asset Allocation based on the customer's age range {ctx.deps.age_range}",
        deps=ctx.deps
    )
    return result.output

# Generic tools for the expert sub-agents
async def calculate_optimal_xirr(fund_category: str) -> float:
    """Calculate the minimum expected XIRR for given fund category. Fund category values are EQ, DT, HY"""
    match fund_category:
        case 'EQ':
            return 12.0
        case 'DT':
            return 7.0
        case 'HY':
            return 10.0
        case _:
            return 0.0

async def get_fund_recommendation(fund_category: str) -> str:
    """Get a recommendation for a fund category that is better in terms of XIRR. Fund category values are EQ, DT, HY"""
    match fund_category:
        case 'EQ':
            return "Axis Bluechip Fund"
        case 'DT':
            return "Parag Parikh Conservative Hybrid Fund"
        case 'HY':
            return "ICICI Prudential Equity & Debt Fund"
        case _:
            return "Invalid fund category"
        
# Expert sub-agent for Equity funds
equity_fund_agent = Agent(
    'claude-sonnet-4-20250514',
    deps_type=PortfolioAnalysis,
    output_type=str,
    system_prompt=(
        'You are an expert at analyzing Equity funds in India.'
        'Use the tool `calculate_optimal_xirr` to find the minimum expected XIRR for EQ fund category' 
        'Use the tool `calculate_equity_xirr` to calculate XIRR of each fund in EQ fund category'
        'If the XIRR of any fund is less than the minimum expected XIRR, Suggest an alternate fund that is better'
        'Use the tool `get_fund_recommendation` to get a recommendation for a fund category that is better'
    ),
    tools=[
        calculate_optimal_xirr,
        get_fund_recommendation,
    ],
)

# agent specific tools using context
@equity_fund_agent.tool
async def calculate_equity_xirr(ctx: RunContext[PortfolioAnalysis]) -> float:
    return calculate_fundwise_xirr(ctx.deps, 'EQ')

# Util functions which are indirectly used by the tools
def calculate_fundwise_xirr(portfolio: PortfolioAnalysis, fund_category: str) -> dict[str, float]:
    """Calculate XIRR of each fund in a given fund category. Fund category values are EQ, DT, HY"""
    portfolio_df = portfolio_to_dataframe(portfolio)
    fund_category_df = portfolio_df[portfolio_df['fund_category'] == fund_category]
    fund_codes = fund_category_df['fund_code'].unique()
    result = {fund_code: calculate_xirr(fund_category_df[fund_category_df['fund_code'] == fund_code]) for fund_code in fund_codes}
    return result

def calculate_xirr(transactions: pd.DataFrame) -> float:
    """Calculates the XIRR for a series of transactions."""
    values = []
    dates = []
    for _, row in transactions.iterrows():
        values.append(-row['units'] * row['unit_price'])
        dates.append(row['date'])

    # Add the current value of the investment
    current_price = transactions['unit_price'].iloc[-1]
    total_units = transactions['units'].sum()
    values.append(total_units * current_price)
    dates.append(datetime.now())

    try:
        result = xirr(dates, values)
        logger.info(f"XIRR for {transactions['fund_code'].iloc[0]} is {result}")
        return result
    except Exception as e:
        print(f"XIRR calculation failed: {e}")
        return 0.0

# More sub-agents called in parallel
debt_fund_agent = Agent(
    'claude-sonnet-4-20250514',
    deps_type=PortfolioAnalysis,
    output_type=str,
    system_prompt=(
        'You are an expert at analyzing Debt funds in India.'
        'Use the tool `calculate_optimal_xirr` to find the minimum expected XIRR for DT fund category' 
        'Use the tool `calculate_debt_xirr` to calculate XIRR of each fund in DT fund category'
        'If the XIRR of any fund is less than the minimum expected XIRR, Suggest an alternate fund that is better'
        'Use the tool `get_fund_recommendation` to get a recommendation for a fund category that is better'
    ),
    tools=[
        calculate_optimal_xirr,
        calculate_fundwise_xirr,
        get_fund_recommendation,
    ],
)

# More sub-agents called in parallel
hybrid_fund_agent = Agent(
    'claude-sonnet-4-20250514',
    deps_type=PortfolioAnalysis,
    output_type=str,
    system_prompt=(
        'You are an expert at analyzing Hybrid funds in India.'
        'Use the tool `calculate_optimal_xirr` to find the minimum expected XIRR for HY fund category' 
        'Use the tool `calculate_hybrid_xirr` to calculate XIRR of each fund in HY fund category'
        'If the XIRR of any fund is less than the minimum expected XIRR, Suggest an alternate fund that is better'
        'Use the tool `get_fund_recommendation` to get a recommendation for a fund category that is better'
    ),
    tools=[
        calculate_optimal_xirr,
        calculate_fundwise_xirr,
        get_fund_recommendation,
    ],
)

# agent specific tools using context
@debt_fund_agent.tool
async def calculate_debt_xirr(ctx: RunContext[PortfolioAnalysis]) -> float:
    """Calculate XIRR of each fund in Debt(DT) fund category"""
    return calculate_fundwise_xirr(ctx.deps, 'DT')

# agent specific tools using context
@hybrid_fund_agent.tool
async def calculate_hybrid_xirr(ctx: RunContext[PortfolioAnalysis]) -> float:
    """Calculate XIRR of each fund in Hybrid(HY) fund category"""
    return calculate_fundwise_xirr(ctx.deps, 'HY')

# Pydantic Models - to be used for structured output later
# class FundAnalysis(BaseModel):
#     """Represents the analysis of a single fund."""
#     fund_name: str = Field(..., description="The name of the fund.")
#     xirr: float = Field(..., description="The calculated XIRR of the fund.")
#     is_performing: bool = Field(..., description="Whether the fund is performing as per ideal returns.")
#     suggestion: str = Field(None, description="Suggestion for a better fund if not performing well.")

# class RatioAnalysis(BaseModel):
#     """Represents the analysis of the portfolio's asset allocation."""
#     current_ratio: dict = Field(..., description="The current asset allocation ratio.")
#     ideal_ratio: dict = Field(..., description="The ideal asset allocation ratio for the age bracket.")
#     suggestion: str = Field(..., description="Suggestion to rebalance the portfolio.")

# More sub-agents called in sequence
asset_allocation_agent = Agent(
    'claude-sonnet-4-20250514',
    deps_type=PortfolioAnalysis,
    output_type=str,
    system_prompt=(
        'You are an expert at analyzing Asset allocation in India.'
        'Use the tool `calculate_current_asset_allocation_ratio` to find the asset allocation across fund categories. Fund categories are Equity(EQ), Debt(DT), Hybrid(HY)'
        'Use the tool `ideal_asset_allocation_ratio` to find the ideal asset allocation across fund categories. Fund categories are Equity(EQ), Debt(DT), Hybrid(HY)'
        'If the current asset allocation is not close to the ideal asset allocation, Suggest a rebalancing plan'
    )
)

@asset_allocation_agent.tool
async def calculate_current_asset_allocation_ratio(ctx: RunContext[PortfolioAnalysis]) -> dict:
    """Calculate the current asset allocation ratio across fund categories"""
    portfolio = portfolio_to_dataframe(ctx.deps)
    total_investment = (portfolio['units'] * portfolio['unit_price']).sum()
    equity_investment = (portfolio[portfolio['fund_category'] == 'EQ']['units'] * portfolio[portfolio['fund_category'] == 'EQ']['unit_price']).sum()
    debt_investment = (portfolio[portfolio['fund_category'] == 'DT']['units'] * portfolio[portfolio['fund_category'] == 'DT']['unit_price']).sum()
    hybrid_investment = (portfolio[portfolio['fund_category'] == 'HY']['units'] * portfolio[portfolio['fund_category'] == 'HY']['unit_price']).sum()

    result = {
        "EQ": equity_investment / total_investment,
        "DT": debt_investment / total_investment,
        "HY": hybrid_investment / total_investment,
    }
    logger.info(f"Current asset allocation ratio: {result}")
    return result

@asset_allocation_agent.tool_plain
async def ideal_asset_allocation_ratio() -> dict:
    """Calculate the ideal asset allocation ratio across fund categories"""
    ideal_ratios = {
        "0-20": {"EQ": 0.8, "DT": 0.1, "HY": 0.1},
        "20-30": {"EQ": 0.7, "DT": 0.2, "HY": 0.1},
        "30-40": {"EQ": 0.6, "DT": 0.2, "HY": 0.2},
        "40-50": {"EQ": 0.5, "DT": 0.4, "HY": 0.1},
        "50-60": {"EQ": 0.4, "DT": 0.5, "HY": 0.1},
        ">60": {"EQ": 0.3, "DT": 0.6, "HY": 0.1},
    }
    logger.info(f"Ideal asset allocation ratio: {ideal_ratios}")
    return ideal_ratios

# util functions
def load_portfolio(filepath: str) -> pd.DataFrame:
    """Loads the portfolio from a CSV file."""
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    return df

async def main():
    """Main function to run the portfolio planner."""
    # Load the portfolio
    portfolio_df = load_portfolio("./data/portfolio.csv")    
    logger.info(f"Loading portfolio from ./data/portfolio.csv")
    logger.info(f"Portfolio loaded with {len(portfolio_df)} records")
    logger.info("Sample records:")
    logger.info(portfolio_df.head())
    deps = PortfolioAnalysis(
        portfolio=[FundTransaction(**record) for record in portfolio_df.to_dict(orient='records')], 
        age_range="30-40"
    )
    result = await financial_planner_agent.run(
        f"""Analyze my portfolio and provide recommendations:
        Portfolio:
        {deps.portfolio}
        
        Age group:
        {deps.age_range}        
        """,
        deps = deps
    )
    print(result.output)
    print(result.usage())
    trace_all_messages(result)

if __name__ == "__main__":
    asyncio.run(main())