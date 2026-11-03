import json

from openai.types.responses import FunctionToolParam

from src.services.orders import get_order

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

def execute_tools(calls):
    results = []
    for call in calls:
        arguments = json.loads(call.arguments)

        if call.name == 'get_order':
            response = get_order(arguments['order_id'])

            results.append({
                "type": "function_call_output",
                "call_id": call.call_id, 
                "output": json.dumps(response)
            })

        else:
            raise ValueError("we don't have that tool")
    return results