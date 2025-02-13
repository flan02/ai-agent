from SimplerLLM.language.llm import LLM.LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from actions import get_seo_page_report
from prompts import react_system_prompt

llm_instance = LLM.create(LLMProvider.OPENAI, model_name="gpt-3.5-turbo")

available_actions = {
    "get_seo_page_report": get_seo_page_report
}

user_query = """
suggest some optimizations tips for www.2kceltics.xyz
"""
# user_query = """ how many images are there on freeaikit.com? """

messages = [
  { "role": "system", "content": react_system_prompt },
  { "role": "user", "content": user_query }
]