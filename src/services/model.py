
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = 'gpt-5-nano'


def call_model(**kwargs):
    return client.responses.create(
        model=MODEL, 
        **kwargs
    )