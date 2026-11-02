from typing import cast

from openai.types.responses import ResponseInputItemParam

from src.PROMPT import INSTRUCTION
from src.services.model import call_model
from src.services.tools import TOOLS, execute_tools


def run_agent(history, customer_message):

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
        if not calls:
            return response.output_text
        

        history.extend(cast(list[ResponseInputItemParam], response.output))

        for result in execute_tools(calls):
            history.append(result.copy())

    
    return "error: agent called tools more times than it should have"


def start_agent():
    history: list[ ResponseInputItemParam] = []

    while True:
        customer_message = input("customer: ")
        if customer_message == "exit": 
            print("good bye old friend")
            break 

        print()
        response = run_agent(history, customer_message)
        print(response)
        print()
