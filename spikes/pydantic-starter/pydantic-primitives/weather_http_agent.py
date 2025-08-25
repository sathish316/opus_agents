import asyncio

from dataclasses import dataclass
from typing import Any

from httpx import AsyncClient
from pydantic import BaseModel

from pydantic_ai import Agent, RunContext

@dataclass
class Deps:
    client: AsyncClient

weather_agent = Agent(
    'openai:gpt-4o',
    instructions = 'Be concise, reply in one sentence',
    deps_type = Deps,
    retries = 3
)

class LatLng(BaseModel):
    lat: float
    lng: float

@weather_agent.tool
async def get_lat_long(ctx: RunContext[Deps], location_description: str) -> LatLng:
    """
    Get the latitude and longitude of a location
    """
    r = await ctx.deps.client.get(
        'https://demo-endpoints.pydantic.workers.dev/latlng',
        params={'location': location_description},
    )
    r.raise_for_status()
    return LatLng.model_validate_json(r.content)

@weather_agent.tool
async def get_weather(ctx: RunContext[Deps], lat: float, lng: float) -> dict[str, Any]:
    """
    Get the weather at a location
    """
    temp_response = await ctx.deps.client.get(
        'https://demo-endpoints.pydantic.workers.dev/number',
        params={'min': 10, 'max': 30},
    ),
    desc_response = await ctx.deps.client.get(
        'https://demo-endpoints.pydantic.workers.dev/weather',
        params={'lat': lat, 'lng': lng},
    )
    return {
        'temperature': f"{temp_response}",
        'description': f"{desc_response}"
    }

async def main():
    async with AsyncClient() as client:
        deps = Deps(client=client)
        result = await weather_agent.run(
            'What is the weather like in London and in Wiltshire?', deps=deps
        )
        print('Response:', result.output)


if __name__ == '__main__':
    asyncio.run(main())