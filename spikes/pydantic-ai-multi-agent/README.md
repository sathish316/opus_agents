# Pydantic AI Multi-Agent Portfolio Planner

This spike demonstrates a multi-agent portfolio planner using PydanticAI. The system uses four agents to analyze a user's investment portfolio:

-   **Equity Expert:** Analyzes equity funds.
-   **Debt Expert:** Analyzes debt funds.
-   **Hybrid Expert:** Analyzes hybrid funds.
-   **Ideal Ratio Expert:** Analyzes the overall asset allocation based on the user's age.

## Setup

1.  **Install dependencies:**

    The dependencies for this project are listed in the `pyproject.toml` file. You can install them using `pip`:

    ```bash
    pip install "pydantic-ai" pandas numpy numpy-financial litellm python-dotenv
    ```

2.  **Set up OpenAI API Key:**

    This project uses OpenAI's GPT-4 model. You need to have an OpenAI API key to run the planner.

    -   Create a file named `.env` in the `spikes/pydantic-ai-multi-agent` directory.
    -   Add the following line to the `.env` file, replacing `"your-api-key"` with your actual key:

        ```
        OPENAI_API_KEY="your-api-key"
        ```

## How to Run

To run the portfolio planner, execute the `main.py` script from the root of the repository:

```bash
python -m spikes.pydantic-ai-multi-agent.main
```

The script will load the sample `portfolio.csv`, run the analysis, and print the results to the console.

## Components

-   **`portfolio.csv`**: A sample CSV file containing portfolio data.
-   **`agents.py`**: Defines the four agents using PydanticAI, including their logic and Pydantic models for structured output.
-   **`main.py`**: The main script that loads the data, sets up the multi-agent system, and runs the analysis.
-   **`pyproject.toml`**: Defines the project's dependencies.
