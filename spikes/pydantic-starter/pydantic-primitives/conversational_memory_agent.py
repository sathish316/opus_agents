from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

# first run
result1 = agent.run_sync('Who is Albert Einstein?')
print(result1.output)

# second run with memory
result2 = agent.run_sync(
    'What was his most famous equation?',
    message_history = result1.new_messages()
    )
print(result2.output)