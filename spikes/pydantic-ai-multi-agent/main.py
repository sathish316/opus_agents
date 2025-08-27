import asyncio
from agents import load_portfolio, setup_multi_agent

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
