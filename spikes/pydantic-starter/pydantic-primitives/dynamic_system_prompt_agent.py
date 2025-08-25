from datetime import date

from pydantic_ai import Agent, RunContext

agent = Agent(
    'openai:gpt-4o',
    deps_type = str,
    system_prompt = "Always prefix the answer with the User's name"
)

@agent.system_prompt
def get_user_name(ctx: RunContext[str]) -> str:
    return f"The user's name is {ctx.deps}"

@agent.system_prompt
def get_date(ctx: RunContext[str]) -> str:
    return f"The date is {date.today()}"

result = agent.run_sync('What is the date today?', deps = 'Travis')
print(result.output)