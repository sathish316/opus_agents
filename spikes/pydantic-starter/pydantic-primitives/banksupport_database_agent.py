from dataclasses import dataclass

from pydantic import BaseModel, Field

from pydantic_ai import Agent, RunContext

class DatabaseConn:
    """
    This is a stub instead of a real database connection.
    """

    @classmethod
    async def customer_name(cls, *, id: int) -> str:
        if id == 123:
            return 'Travis'
    
    @classmethod
    async def customer_balance(cls, *, id: int) -> float:
        if id == 123:
            return 123.45
        
@dataclass
class Deps:
    customer_id: int
    db: DatabaseConn

class SupportOutput(BaseModel):
    support_advice: str = Field(description = 'The advice to give to the customer')

support_agent = Agent(
    'openai:gpt-4o',
    deps_type = Deps,
    output_type = SupportOutput,
    system_prompt = (
        'You are a support agent in our bank.'
        'Give the customer support for the queries they have.'
        'Use a friendly tone to respond and prefix responses respectfully with the customer name'
    )
)

@support_agent.tool
async def get_customer_name(ctx: RunContext[Deps]) -> str:
    """
    Get the customer name from the database
    """
    return await ctx.deps.db.customer_name(id = ctx.deps.customer_id)

@support_agent.tool
async def get_customer_balance(ctx: RunContext[Deps]) -> float:
    """
    Get the customer balance from the database
    """
    return await ctx.deps.db.customer_balance(id = ctx.deps.customer_id)

result = support_agent.run_sync(
    'What is my balance?',
    deps = Deps(customer_id = 123, db = DatabaseConn())
)
print(result.output)