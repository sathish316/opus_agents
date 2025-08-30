from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from llm_helper import trace_all_messages
        
@dataclass
class TravelSearchRequest:
    destination: str
    month: str


travel_planner_agent = Agent(
    'openai:gpt-4o',
    deps_type=TravelSearchRequest,
    output_type=str,
    system_prompt=(
        'Use the `trip_advisor` to get suggestions on places to visit.'
        'Choose the best place to visit.'
        'You must return just a single place to visit.'
        'Dont suggest Eiffel Tower'
    ),
)

trip_advisor_agent = Agent(
    'openai:gpt-4o',
    output_type=list[str],
)

@travel_planner_agent.tool
async def trip_advisor(ctx: RunContext[None], count: int) -> list[str]:
    r = await trip_advisor_agent.run(
        f'Get {count} places to visit at {ctx.deps.destination} in the month of {ctx.deps.month}'
    )
    return r.output

result = travel_planner_agent.run_sync(
    "Suggest a place to visit",
    deps = TravelSearchRequest(destination = "Paris", month = "December")
)

print(result.output)
trace_all_messages(result)




