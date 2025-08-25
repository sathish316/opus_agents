import os
import asyncio

from pydantic import BaseModel, Field

from pydantic_ai import Agent, RunContext

from typing import Annotated
from typing_extensions import NotRequired, TypedDict

class MyModel(BaseModel):
    city: str
    country: str

model = 'openai:gpt-4o'
agent = Agent(model, output_type = MyModel)

result = agent.run_sync('Which is the windy city in USA')
print(result.output)

class Whale(TypedDict):
    name: str
    length: Annotated[
        float, Field(description = 'Average length of whale in meters')
    ]
    weight: NotRequired[
        Annotated[
            float, 
            Field(description = 'Average weight of whale in kilograms', ge=50)
        ]
    ]
    ocean: NotRequired[str]
    description: NotRequired[Annotated[str, Field(description = 'A short description of the whale')]]

model = 'openai:gpt-4o'
agent = Agent(model, output_type = list[Whale])

#result = agent.run_stream('Generate me details of 5 species of Whales')
async def main():
    async with agent.run_stream('Generate me details of 5 species of Whales') as result:
        async for whale in result.stream():
            print(whale)

if __name__ == '__main__':
    asyncio.run(main())
