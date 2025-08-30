import os
import pandas as pd
import numpy_financial as npf
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_ai import MultiAgent, Logic, LLM
from dotenv import load_dotenv
import asyncio

#load_dotenv()

# 1. Data Loading
def load_portfolio(filepath: str) -> pd.DataFrame:
    """Loads the portfolio from a CSV file."""
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# 2. XIRR Calculation
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

# 3. Pydantic Models
class FundAnalysis(BaseModel):
    """Represents the analysis of a single fund."""
    fund_name: str = Field(..., description="The name of the fund.")
    xirr: float = Field(..., description="The calculated XIRR of the fund.")
    is_performing: bool = Field(..., description="Whether the fund is performing as per ideal returns.")
    suggestion: str = Field(None, description="Suggestion for a better fund if not performing well.")

class PortfolioAnalysis(BaseModel):
    """Represents the analysis of a portfolio."""
    funds: list[FundAnalysis] = Field(..., description="A list of fund analyses.")

class RatioAnalysis(BaseModel):
    """Represents the analysis of the portfolio's asset allocation."""
    current_ratio: dict = Field(..., description="The current asset allocation ratio.")
    ideal_ratio: dict = Field(..., description="The ideal asset allocation ratio for the age bracket.")
    suggestion: str = Field(..., description="Suggestion to rebalance the portfolio.")

# 4. Agent Definitions
class EquityExpert(Logic):
    """An expert on equity funds in India."""

    def __init__(self, portfolio: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.portfolio = portfolio
        self.ideal_return = 12.0
        self.suggestion = "Consider investing in Axis Bluechip Fund for better returns."

    async def run(self) -> PortfolioAnalysis:
        equity_funds = self.portfolio[self.portfolio['fund_code'].str.startswith('EQ')]
        analysis = []
        for fund_name, transactions in equity_funds.groupby('fund_name'):
            xirr = calculate_xirr(transactions)
            is_performing = xirr >= self.ideal_return
            suggestion = self.suggestion if not is_performing else None
            analysis.append(FundAnalysis(fund_name=fund_name, xirr=xirr, is_performing=is_performing, suggestion=suggestion))
        return PortfolioAnalysis(funds=analysis)

class DebtExpert(Logic):
    """An expert on debt funds in India."""

    def __init__(self, portfolio: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.portfolio = portfolio
        self.ideal_return = 7.0
        self.suggestion = "Consider investing in Parag Parikh Conservative Hybrid Fund for stable returns."

    async def run(self) -> PortfolioAnalysis:
        debt_funds = self.portfolio[self.portfolio['fund_code'].str.startswith('DT')]
        analysis = []
        for fund_name, transactions in debt_funds.groupby('fund_name'):
            xirr = calculate_xirr(transactions)
            is_performing = xirr >= self.ideal_return
            suggestion = self.suggestion if not is_performing else None
            analysis.append(FundAnalysis(fund_name=fund_name, xirr=xirr, is_performing=is_performing, suggestion=suggestion))
        return PortfolioAnalysis(funds=analysis)

class HybridExpert(Logic):
    """An expert on hybrid funds in India."""

    def __init__(self, portfolio: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.portfolio = portfolio
        self.ideal_return = 10.0
        self.suggestion = "Consider investing in ICICI Prudential Equity & Debt Fund for balanced growth."

    async def run(self) -> PortfolioAnalysis:
        hybrid_funds = self.portfolio[self.portfolio['fund_code'].str.startswith('HY')]
        analysis = []
        for fund_name, transactions in hybrid_funds.groupby('fund_name'):
            xirr = calculate_xirr(transactions)
            is_performing = xirr >= self.ideal_return
            suggestion = self.suggestion if not is_performing else None
            analysis.append(FundAnalysis(fund_name=fund_name, xirr=xirr, is_performing=is_performing, suggestion=suggestion))
        return PortfolioAnalysis(funds=analysis)

class IdealRatioExpert(Logic):
    """An expert on ideal asset allocation ratios."""

    def __init__(self, portfolio: pd.DataFrame, age_bracket: str, **kwargs):
        super().__init__(**kwargs)
        self.portfolio = portfolio
        self.age_bracket = age_bracket
        self.ideal_ratios = {
            "<30": {"Equity": 0.6, "Debt": 0.3, "Hybrid": 0.1},
            "30-50": {"Equity": 0.5, "Debt": 0.4, "Hybrid": 0.1},
            ">50": {"Equity": 0.3, "Debt": 0.6, "Hybrid": 0.1},
        }

    def calculate_current_ratio(self) -> dict:
        total_investment = (self.portfolio['units'] * self.portfolio['unit_price']).sum()
        equity_investment = (self.portfolio[self.portfolio['fund_code'].str.startswith('EQ')]['units'] * self.portfolio[self.portfolio['fund_code'].str.startswith('EQ')]['unit_price']).sum()
        debt_investment = (self.portfolio[self.portfolio['fund_code'].str.startswith('DT')]['units'] * self.portfolio[self.portfolio['fund_code'].str.startswith('DT')]['unit_price']).sum()
        hybrid_investment = (self.portfolio[self.portfolio['fund_code'].str.startswith('HY')]['units'] * self.portfolio[self.portfolio['fund_code'].str.startswith('HY')]['unit_price']).sum()

        return {
            "Equity": equity_investment / total_investment,
            "Debt": debt_investment / total_investment,
            "Hybrid": hybrid_investment / total_investment,
        }

    async def run(self) -> RatioAnalysis:
        current_ratio = self.calculate_current_ratio()
        ideal_ratio = self.ideal_ratios.get(self.age_bracket, self.ideal_ratios["30-50"])

        suggestion = "Your portfolio allocation is optimal."
        # This is a simplified check. A more detailed check would compare each category.
        if not all(abs(current_ratio[k] - ideal_ratio[k]) < 0.1 for k in ideal_ratio):
            suggestion = f"Your portfolio is not optimally allocated for the {self.age_bracket} age bracket. Consider rebalancing to achieve the ideal ratio of {ideal_ratio}."

        return RatioAnalysis(
            current_ratio=current_ratio,
            ideal_ratio=ideal_ratio,
            suggestion=suggestion,
        )

# 5. Multi-agent setup
def setup_multi_agent(portfolio: pd.DataFrame, age_bracket: str) -> MultiAgent:
    """Sets up the multi-agent system."""

    llm = LLM(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4-turbo-preview",
        temperature=0,
        max_tokens=2000,
    )

    equity_expert = EquityExpert(portfolio=portfolio, llm=llm)
    debt_expert = DebtExpert(portfolio=portfolio, llm=llm)
    hybrid_expert = HybridExpert(portfolio=portfolio, llm=llm)
    ideal_ratio_expert = IdealRatioExpert(portfolio=portfolio, age_bracket=age_bracket, llm=llm)

    agent = MultiAgent(
        llm=llm,
        logics=[equity_expert, debt_expert, hybrid_expert, ideal_ratio_expert],
        description="A multi-agent system for portfolio analysis.",
    )
    return agent

async def main():
    """Main function to run the portfolio planner."""
    # Load the portfolio
    portfolio = load_portfolio("spikes/pydantic-ai-multi-agent/portfolio.csv")

    # Set the age bracket
    age_bracket = "30-50"

    # Set up the multi-agent system
    multi_agent = setup_multi_agent(portfolio, age_bracket)

    # Define the prompt
    prompt = "Analyze my portfolio and provide suggestions for improvement."

    # Run the agent
    print("Analyzing portfolio... This may take a moment.")
    result = await multi_agent.run(prompt)

    # Print the result
    print("\n--- Portfolio Analysis ---")
    print(result)
    print("------------------------")


if __name__ == "__main__":
    # Note: You need to have OPENAI_API_KEY set in your environment variables
    # or in a .env file for this to work.
    # You can get a key from https://platform.openai.com/account/api-keys

    # To run this script:
    # 1. Create a .env file in this directory
    # 2. Add the following line to it:
    #    OPENAI_API_KEY="your-api-key"
    # 3. Run the script from the root of the repository:
    #    python -m spikes.pydantic-ai-multi-agent.main

    asyncio.run(main())
