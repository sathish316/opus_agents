from dataclasses import dataclass
import asyncio
import httpx

from pydantic_ai import Agent, RunContext

@dataclass
class TravelSearchHelper:
    http_client: httpx.AsyncClient
    api_key: str

travel_planner_agent = Agent(
    'openai:gpt-4o',
    deps_type=TravelSearchHelper,
    system_prompt=(
        'Use the `trip_advisor` to get suggestions on places to visit.'
        'Choose the best place to visit.'
        'You must return just a single place to visit.'
    ),
)

trip_advisor_agent = Agent(
    'openai:gpt-4o',
    deps_type=TravelSearchHelper,
    output_type=list[str],
    system_prompt=(
        'Use the "find_places" tool to get some places to visit at a given place and month'
        'then extract each place into a list.'
    ),
)

@travel_planner_agent.tool
async def trip_advisor(ctx: RunContext[None], count: int) -> list[str]:
    r = await trip_advisor_agent.run(
        f'Get {count} places to visit at a given place and month',
        deps=ctx.deps,
    )
    return r.output

@trip_advisor_agent.tool
async def find_places(ctx: RunContext[TravelSearchHelper], count: int) -> str:
    response = await ctx.deps.http_client.get(
        'https://example.com',
        params={'count': count},
                headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
    )
    response.raise_for_status()
    return response.text

async def main():
    async with httpx.AsyncClient() as client:
        deps = TravelSearchHelper(client, "foobar")
        result = await travel_planner_agent.run(
            "Suggest a place to visit in Paris in the month of August",
            deps = deps
        )
        print(result.output)
        print(result.usage())


if __name__ == "__main__":
    asyncio.run(main())


