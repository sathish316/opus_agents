import asyncio
from dataclasses import dataclass
from datetime import timedelta
from typing import List

from temporalio import workflow

from shared import TranslateInput

with workflow.unsafe.imports_passed_through():
    from activities import translate_phrase

@workflow.defn
class TranslateWorkflow:
    @workflow.run
    async def run(self, input: TranslateInput) -> str:
        # run activity
        return await workflow.execute_activity(
            translate_phrase,
            input,
            schedule_to_close_timeout=timedelta(seconds=30),
        )
    
@workflow.defn
class TranslateSuperWorkflow:
    @workflow.run
    async def run(self, input: TranslateInput) -> str:
        # run activity
        return await workflow.execute_child_workflow(
            TranslateWorkflow.run,
            input,
            schedule_to_close_timeout=timedelta(seconds=30),
        )
    

