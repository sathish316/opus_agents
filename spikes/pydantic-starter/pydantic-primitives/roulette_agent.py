from pydantic_ai import Agent, RunContext

roulette_agent = Agent(
    'openai:gpt-4o',
    deps_type = int,
    output_type = bool,
    system_prompt = (
        'Use the `roulette_wheel` function to see if the player has won based on the number that they provide'
    )
)

@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> bool:
    """check if the square is a winner"""
    return 'winner' if square == ctx.deps else 'loser'

# seed the winning square
success_square = 18
result = roulette_agent.run_sync(
    'Put my money on number eighteen',
    deps = success_square
)
print(result)

result = roulette_agent.run_sync(
    'I bet five is the winner',
    deps = success_square
)
print(result)