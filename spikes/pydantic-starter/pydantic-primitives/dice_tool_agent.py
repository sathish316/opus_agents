import random

from pydantic_ai import Agent, RunContext

agent = Agent(
    'openai:gpt-4o',
    deps_type = str,
    system_prompt = (
        "You are a Dice game, You should roll the die and see if the number matches User's guess."
        "If so, tell them they'e a winner."
        "Use the player's name in response"
    )
)

@agent.tool_plain
def roll_dice() -> str:
    """Roll a six-sided die"""
    return str(random.randint(1, 6))

@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name"""
    return ctx.deps

dice_result = agent.run_sync("My guess is 4", deps = 'Travis')
print(dice_result.output)