from typing import Literal, Union

from pydantic import BaseModel, Field
from rich.prompt import Prompt

from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage
from llm_helper import trace_all_messages

class FlightDetails(BaseModel):
    flight_number: str

class Failed(BaseModel):
    """"Unable to find a satisfactory flight"""

flight_search_agent = Agent[None, Union[FlightDetails, Failed]](
    'openai:gpt-4o',
    output_type=Union[FlightDetails, Failed],
    system_prompt=(
        'Use the `flight_search` tool to find a flight '
        'from the given origin to the given destination'
    )
)

@flight_search_agent.tool
async def flight_search(ctx: RunContext[None], origin: str, destination: str) -> Union[FlightDetails, None]:
    return FlightDetails(flight_number='123456')

async def find_flight() -> Union[FlightDetails, None]:  
    message_history: Union[list[ModelMessage], None] = None
    for _ in range(3):
        prompt = Prompt.ask(
            'Where would you like to fly from and to?',
        )
        result = await flight_search_agent.run(
            prompt,
            message_history=message_history,
        )
        print("=== Trace of find_flight ===")
        trace_all_messages(result)
        if isinstance(result.output, FlightDetails):
            return result.output
        else:
            message_history = result.all_messages(
                output_tool_return_content='Please try again.'
            )

class SeatPreference(BaseModel):
    row: int = Field(ge=1, le=30)
    seat: Literal['A', 'B', 'C', 'D', 'E', 'F']

seat_preference_agent = Agent[None, Union[SeatPreference, Failed]](
    'openai:gpt-4o',
    output_type=Union[SeatPreference, Failed],
    system_prompt=(
        "Extract the user's seat preference. "
        'Seats A and F are window seats.'
        'Row 1 is the front row and has extra legroom'
        'Rows 14 and 20 also have extra leg room'
    )
)

async def find_seat() -> SeatPreference:  
    message_history: Union[list[ModelMessage], None] = None
    while True:
        answer = Prompt.ask('What seat would you like?')

        result = await seat_preference_agent.run(
            answer,
            message_history=message_history,
        )
        print("=== Trace of find_seat ===")
        trace_all_messages(result)
        if isinstance(result.output, SeatPreference):
            return result.output
        else:
            print('Could not understand seat preference. Please try again.')
            message_history = result.all_messages()

async def main():
    opt_flight_details = await find_flight()
    if opt_flight_details is not None:
        seat_preference = await find_seat()
        print(f'You are flying on flight {opt_flight_details.flight_number} in seat {seat_preference.row}{seat_preference.seat}')
    else:
        print('No flight found.')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())