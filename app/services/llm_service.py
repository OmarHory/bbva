from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.config.settings import settings

llm = ChatOpenAI(
    model_name=settings.openai.model,
    temperature=0,
    openai_api_key=settings.openai.api_key
)

def run_agent(prompt: str, user_input: str, schema = None) -> dict:
    system_message = SystemMessage(content=prompt)
    human_message = HumanMessage(content=user_input)
    if schema is not None:
        response = llm.with_structured_output(schema).invoke([system_message, human_message])
    else:
        response = llm.invoke([system_message, human_message])
    
    return response