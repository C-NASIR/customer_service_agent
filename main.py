import json
import os
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import FunctionToolParam, ResponseInputItemParam

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = 'gpt-5-nano'

ORDERS = {
    "123": {
        "status": "shipped", 
        "arrival": "friday"
    },
    "456": {
        "status": "processing", 
        "arrival": None
    }
}

def get_order(order_id):
    return ORDERS.get(order_id, {"error": "no order found"})


TOOLS: list[FunctionToolParam] = [
    {
        "type": "function", 
        "name": "get_order", 
        "description": "returns order status and arrival date", 
        "parameters": {
            "type": "object", 
            "properties": {
                "order_id": {"type": "string"}
            }, 
            "required": ['order_id'], 
            "additionalProperties": False
        }, 
        "strict": True
    }
]

POLICY = "shoes can be returned upto 30 days"

INSTRUCTION = f"""
you are a customer service assisstant

Store Policy: {POLICY}

don't be verbose. 
don't recommend next steps
"""

messages: list[ ResponseInputItemParam] = []

def run_agent(customer_message):

    messages.append({
        "role": "user", 
        "content": customer_message
    })

    for step in range(5):
        response = client.responses.create(
            model=MODEL, 
            instructions=INSTRUCTION, 
            input=messages, 
            tools=TOOLS
        )

        calls = [item for item in response.output if item.type == 'function_call']
        if not calls:
            return response.output_text
        

        messages.extend(cast(list[ResponseInputItemParam], response.output))

        for call in calls:
            arguments = json.loads(call.arguments)

            if call.name == 'get_order':
                result = get_order(arguments['order_id'])

                messages.append({
                    "type": "function_call_output",
                    "call_id": call.call_id, 
                    "output": json.dumps(result)
                })

            else:
                raise ValueError("we don't have that tool")
    
    return "error: agent called tools more times than it should have"


if __name__ == "__main__":

    while True:
        message = input("customer: ")
        if message == "exit": 
            print("good bye old friend")
            break 

        print()
        response = run_agent(message)
        print(response)
        print()


