def trace_all_messages(result):
    """
    Helper function to log all messages from a pydantic-ai agent result.
    
    Args:
        result: The result object from a pydantic-ai agent run
    """
    print("\n=== All Messages ===")
    for i, message in enumerate(result.all_messages(), 1):
        print(f"\nMessage {i}:")
        # print(message)
        
        for j, part in enumerate(message.parts, 1):
            if part.part_kind == 'system-prompt':
                print(f"(System): {part.content}\n")
            elif part.part_kind == 'user-prompt':
                print(f"(User): {part.content}\n")
            elif part.part_kind == 'tool-call':
                print(f"(Tool Call): {part.tool_name} - {part.args}\n")
            elif part.part_kind == 'tool-return':
                print(f"(Tool Result): {part.content}\n")
            elif part.part_kind == 'text':
                print(f"(Model): {part.content}\n") 