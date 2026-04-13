import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Configure la connexion via OpenRouter"""
    return ChatOpenAI(
        model=os.getenv("MODEL_NAME", "qwen/qwen-plus"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

def simple_chain(prompt_template: str, inputs: dict):
    """Chaîne simple : Prompt -> LLM -> Résultat"""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    return chain.invoke(inputs)