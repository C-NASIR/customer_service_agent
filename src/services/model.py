
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = 'gpt-5-nano'
MODEL_WINDOW = 400_0000
MAX_OUTPUT_TOKENS = 128_000
SOFT_LIMIT = 0.75
HARD_LIMIT = 0.95

def call_model(**kwargs):
    return client.responses.create(
        model=MODEL, 
        **kwargs
    )

def call_compact(context, *, instructions):
    return client.responses.compact(
        model=MODEL, 
        input=context, 
        instructions=instructions
    )

def count_input_tokens(context, *, instructions, tools):
    return client.responses.input_tokens.count(
        model=MODEL,
        input=context, 
        instructions=instructions, 
        tools=tools
    ).input_tokens

def compact_if_we_should(context, *, instructions, tools, at_clean_boundary):
    tokens = count_input_tokens(context, instructions=instructions, tools=tools)
    if tokens >= MODEL_WINDOW:
        raise ValueError("Context is too large to compact safely")
    
    used = tokens / MODEL_WINDOW
    if used < HARD_LIMIT and not (used >= SOFT_LIMIT and at_clean_boundary):
        return context
    
    compacted = call_compact(context, instructions=instructions)
    # Keep every returned item, serialized for our JSON conversation
    replacement = [item.model_dump(exclude_none=True) for item in compacted.output]
    tokens = count_input_tokens(replacement, instructions=instructions, tools=tools)
    if tokens + MAX_OUTPUT_TOKENS > MODEL_WINDOW:
        raise ValueError("Compaction did not leave enough room for the next response")
    
    return replacement


