from dataclasses import dataclass

@dataclass
class TranslateInput:
    phrase: str
    language: str

TASK_QUEUE_NAME = "translate-task-queue"