from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from temporalio import activity

from langchain.prompts import ChatPromptTemplate
from shared import TranslateInput

@activity.defn
async def translate_phrase(input: TranslateInput) -> str:
    # Langchain agent flow
    # define prompt
    template = """
You are a helpful assistant who translates between languages.
Translate the following phrase into the specified language: {phrase}
Language: {language}
    """
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", "Translate")
        ]
    )
    # define model
    model = ChatOpenAI()
    # create chain
    chain = chat_prompt | model
    # invoke chain asynchronously
    print(f"Translating phrase: {input.phrase} to {input.language}")
    result = await chain.ainvoke({"phrase": input.phrase, "language": input.language})
    return dict(result).get("content") or ""
