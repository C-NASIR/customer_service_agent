from src.services.conversations import load_conversation, save_conversations
from src.db import db_init
from typing import cast

from openai.types.responses import ResponseInputItemParam

from src.PROMPT import INSTRUCTION
from src.services.model import call_model
from src.services.tools import TOOLS, execute_tools


def run_agent(history, customer_message, conversation_id):

    history.append({
        "role": "user", 
        "content": customer_message
    })

    for step in range(5):
        response = call_model(
            instructions=INSTRUCTION, 
            input=history, 
            tools=TOOLS
        )

        calls = [item for item in response.output if item.type == 'function_call']

        history.extend([
            item.model_dump(exclude_none=True)
            for item in response.output
        ])

        if not calls:
            save_conversations(conversation_id, history)
            return response.output_text
        
        for result in execute_tools(calls):
            history.append(result.copy())
    
    save_conversations(conversation_id, history)
    return "error: agent called tools more times than it should have"


def start_agent():

    db_init()

    conversation_id = '123'

    history: list[ ResponseInputItemParam] = load_conversation(conversation_id)

    while True:
        customer_message = input("customer: ")
        if customer_message == "exit": 
            print("good bye old friend")
            break 

        print()
        response = run_agent(history, customer_message, conversation_id)
        print(response)
        print()
