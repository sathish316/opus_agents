import asyncio

from activities import translate_phrase
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import TranslateWorkflow, TranslateSuperWorkflow
from shared import TASK_QUEUE_NAME, TranslateInput

interrupt_event = asyncio.Event()

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[TranslateWorkflow, TranslateSuperWorkflow],
        activities=[translate_phrase],
    )
    print("Worker started")
    await worker.run()
    try:
        await interrupt_event.wait()
    except asyncio.CancelledError:
        await client.close()
        print("Worker stopped")
    finally:
        await client.close()
        print("Worker stopped")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nInterrupt received, shutting down...\n")
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())
