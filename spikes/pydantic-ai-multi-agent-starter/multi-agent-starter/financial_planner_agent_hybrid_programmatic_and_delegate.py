import random
import pandas as pd
import numpy_financial as npf
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import asyncio
from dataclasses import dataclass

@dataclass
class Portfolio:
    age_bracket: str = Field(..., description="The age bracket of the customer")
    portfolio: list[dict] = Field(..., description="The portfolio of the customer. Portfolio is a list of rows."
                                  "Each row is a fund transaction record.")

def portfolio_to_dataframe(portfolio: Portfolio) -> pd.DataFrame:
    """Convert a Portfolio object to a pandas DataFrame."""
    df = pd.DataFrame(portfolio.portfolio)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

# class FundTransaction(BaseModel):
#     """Represents a single fund transaction record."""
#     date: datetime = Field(..., description="The transaction date")
#     fund_category: str = Field(..., description="The category of the fund")
#     fund_code: str = Field(..., description="The code of the fund")
#     fund_name: str = Field(..., description="The name of the fund")
#     transaction_type: str = Field(..., description="The type of transaction")
#     units: float = Field(..., description="Number of units transacted")
#     unit_price: float = Field(..., description="Price per unit at the time of transaction")
#     transaction_amount: float = Field(..., description="The amount of the transaction")

# def dict_to_fund_transaction(data: dict) -> FundTransaction:
#     """Convert a dictionary to a FundTransaction object."""
#     return FundTransaction(
#         date=pd.to_datetime(data['Date']).to_pydatetime(),
#         fund_category=data['fund_category'],
#         fund_code=data['fund_code'],
#         fund_name=data['fund_name'],
#         transaction_type=data['transaction_type'],
#         units=float(data['units']),
#         unit_price=float(data['unit_price']),
#         transaction_amount=float(data['units']) * float(data['unit_price'])
#     )


# Planner agent that co-ordinates with the expert agents
financial_planner_agent = Agent(
    'openai:gpt-4o',
    deps_type=Portfolio,
    output_type=str,
    system_prompt=(
        'You are a Financial Planner.'
        'You are given a portfolio of the customer.'
        'You are also given a customer profile like age range.'
        'You have a team of Expert agents for each fund category - Equit, Debt, Hybrid.'
        'Use the tool `analyze_fund_category` to perform analysis on the portfolio for a given fund category.'
        'You have an Expert on Asset Allocation. Use the tool `analyze_asset_allocation` to perform analysis on the portfolio given a customer profile like age range.'
        'Your job is to use the tools to perform analysis on the portfolio and provide a report of suggestions.'
        # "Use the tool `roll_dice` to roll a six-sided die and rate how good the portfolio is."
    ),
)

@financial_planner_agent.tool_plain
def roll_dice() -> str:
    """Roll a six-sided die"""
    return str(random.randint(1, 6))

# Tool to link planner agent with sub-agents
@financial_planner_agent.tool
async def analyze_fund_category(ctx: RunContext[Portfolio], fund_category: str) -> str:
    if fund_category == 'EQ':
        return await equity_fund_agent.run(ctx.deps)
    elif fund_category == 'DT':
        return await debt_fund_agent.run(ctx.deps)
    elif fund_category == 'HY':
        return await hybrid_fund_agent.run(ctx.deps)
    else:
        return 'Invalid fund category'

# Another Tool to link planner agent with sub-agent
@financial_planner_agent.tool
async def analyze_asset_allocation(ctx: RunContext[Portfolio], age_range: str) -> str:
    return await asset_allocation_agent.run(ctx.deps, age_range)

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
    'openai:gpt-4o',
    deps_type=Portfolio,
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
async def calculate_equity_xirr(ctx: RunContext[Portfolio]) -> float:
    return calculate_fundwise_xirr(ctx.deps, 'EQ')

# Util functions which are indirectly used by the tools
def calculate_fundwise_xirr(portfolio: Portfolio, fund_category: str) -> dict[str, float]:
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
        dates.append(row['Date'])

    # Add the current value of the investment
    current_price = transactions['unit_price'].iloc[-1]
    total_units = transactions['units'].sum()
    values.append(total_units * current_price)
    dates.append(datetime.now())

    try:
        return npf.xirr(values, dates) * 100
    except:
        return 0.0

# More sub-agents called in parallel
debt_fund_agent = Agent(
    'openai:gpt-4o',
    deps_type=Portfolio,
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
    'openai:gpt-4o',
    deps_type=Portfolio,
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
async def calculate_debt_xirr(ctx: RunContext[Portfolio]) -> float:
    return calculate_fundwise_xirr(ctx.deps, 'DT')

# agent specific tools using context
@hybrid_fund_agent.tool
async def calculate_hybrid_xirr(ctx: RunContext[Portfolio]) -> float:
    return calculate_fundwise_xirr(ctx.deps, 'HY')

# Pydantic Models - to be used for structured output later
# class FundAnalysis(BaseModel):
#     """Represents the analysis of a single fund."""
#     fund_name: str = Field(..., description="The name of the fund.")
#     xirr: float = Field(..., description="The calculated XIRR of the fund.")
#     is_performing: bool = Field(..., description="Whether the fund is performing as per ideal returns.")
#     suggestion: str = Field(None, description="Suggestion for a better fund if not performing well.")

# class PortfolioAnalysis(BaseModel):
#     """Represents the analysis of a portfolio."""
#     funds: list[FundAnalysis] = Field(..., description="A list of fund analyses.")

# class RatioAnalysis(BaseModel):
#     """Represents the analysis of the portfolio's asset allocation."""
#     current_ratio: dict = Field(..., description="The current asset allocation ratio.")
#     ideal_ratio: dict = Field(..., description="The ideal asset allocation ratio for the age bracket.")
#     suggestion: str = Field(..., description="Suggestion to rebalance the portfolio.")

# Generic tools for expert sub-agent
def calculate_current_asset_allocation_ratio(portfolio_input: Portfolio) -> dict:
    portfolio = portfolio_to_dataframe(portfolio_input)
    total_investment = (portfolio['units'] * portfolio['unit_price']).sum()
    equity_investment = (portfolio[portfolio['fund_category'] == 'EQ']['units'] * portfolio[portfolio['fund_category'] == 'EQ']['unit_price']).sum()
    debt_investment = (portfolio[portfolio['fund_category'] == 'DT']['units'] * portfolio[portfolio['fund_category'] == 'DT']['unit_price']).sum()
    hybrid_investment = (portfolio[portfolio['fund_category'] == 'HY']['units'] * portfolio[portfolio['fund_category'] == 'HY']['unit_price']).sum()

    return {
        "EQ": equity_investment / total_investment,
        "DT": debt_investment / total_investment,
        "HY": hybrid_investment / total_investment,
    }

def ideal_asset_allocation_ratio() -> dict:
    ideal_ratios = {
        "0-20": {"EQ": 0.8, "DT": 0.1, "HY": 0.1},
        "20-30": {"EQ": 0.7, "DT": 0.2, "HY": 0.1},
        "30-40": {"EQ": 0.6, "DT": 0.2, "HY": 0.2},
        "40-50": {"EQ": 0.5, "DT": 0.4, "HY": 0.1},
        "50-60": {"EQ": 0.4, "DT": 0.5, "HY": 0.1},
        ">60": {"EQ": 0.3, "DT": 0.6, "HY": 0.1},
    }

# More sub-agents called in sequence
asset_allocation_agent = Agent(
    'openai:gpt-4o',
    deps_type=Portfolio,
    output_type=str,
    system_prompt=(
        'You are an expert at analyzing Asset allocation in India.'
        'Use the tool `calculate_current_asset_allocation_ratio` to find the asset allocation across fund categories. Fund categories are EQ, DT, HY'
        'Use the tool `ideal_asset_allocation_ratio` to find the ideal asset allocation across fund categories. Fund categories are EQ, DT, HY'
        'If the current asset allocation is not close to the ideal asset allocation, Suggest a rebalancing plan'
    ),
    tools=[
        calculate_current_asset_allocation_ratio,
        ideal_asset_allocation_ratio,
    ],
)

# util functions
def load_portfolio(filepath: str) -> pd.DataFrame:
    """Loads the portfolio from a CSV file."""
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

async def main():
    """Main function to run the portfolio planner."""
    # Set the age bracket
    age_bracket = "30-40"

    # Load the portfolio
    portfolio_df = load_portfolio("./data/portfolio.csv")
    portfolio = Portfolio(portfolio=portfolio_df.to_dict(orient='records'), age_bracket=age_bracket)

    result = await financial_planner_agent.run(
        "Analyze my portfolio and provide suggestions for improvement.",
        deps = portfolio
    )
    print(result.output)
    print(result.usage())
    print("\n=== All Messages ===")
    for i, message in enumerate(result.all_messages(), 1):
        # print(f"\nMessage {i}:")
        # print(message)
        
        for j, part in enumerate(message.parts, 1):
            if part.part_kind == 'system-prompt':
                print(f"(System): {part.content}\n")
            elif part.part_kind == 'user-prompt':
                print(f"(User): {part.content}\n")
            
            # print("\n=== Tool Calls ===")
            # if message.hasattr('tool_calls'): 
            #     for tool_call in message.tool_calls:
            #         print(f"  Tool Call: {tool_call}")
            #         print(f"    Tool Name: {tool_call.name}")
            #         print(f"    Tool Args: {tool_call.args}")
            #         print(f"    Tool Result: {tool_call.result}")
    # print(result.all_messages())

if __name__ == "__main__":
    asyncio.run(main())