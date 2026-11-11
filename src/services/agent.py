from copy import deepcopy

from src.db import db_init
from src.PROMPT import INSTRUCTION
from src.services.conversations import load_conversation, save_conversations
from src.services.model import call_model, compact_if_we_should
from src.services.tools import TOOLS, execute_tools


def run_agent(history, context, customer_message, conversation_id):

    message = {
        "role": "user", 
        "content": customer_message
    }

    history.append(message)
    context.append(deepcopy(message))

    for step in range(5):
        context[:] = compact_if_we_should(
            context, 
            instructions=INSTRUCTION, 
            tools=TOOLS, 
            at_clean_boundary= step == 0
        )

        response = call_model(
            instructions=INSTRUCTION, 
            input=context, 
            tools=TOOLS
        )

        calls = [item for item in response.output if item.type == 'function_call']

        output = [
            item.model_dump(exclude_none=True)
            for item in response.output
        ]
        history.extend(output)
        context.extend(deepcopy(output))

        if not calls:
            save_conversations(conversation_id, history, context)
            return response.output_text
        
        for result in execute_tools(calls):
            history.append(result.copy())
            context.append(deepcopy(result))
    
    save_conversations(conversation_id, history, context)
    return "error: agent called tools more times than it should have"


def start_agent():

    db_init()

    conversation_id = '123'

    history, context = load_conversation(conversation_id)

    while True:
        customer_message = input("customer: ")
        if customer_message == "exit": 
            print("good bye old friend")
            break 

        print()
        response = run_agent(history, context, customer_message, conversation_id)
        print(response)
        print()
