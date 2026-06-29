import os
from dotenv import load_dotenv
from pydantic.deprecated import tools
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


parser = StrOutputParser()


@tool
def crear_tweet(query:str)-> str:
    """ esta herramienta la vas a utilizar cuando  l cliente desee realizar una publicacion en tweeter
        deberas de hacer un tweet chistoso acerda del tema que quiera el cleinte
    """
    return f"tweet para el: {query}"


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[crear_tweet],
    system_prompt="eres un asistente llamado albert que le vas a  ayudar a usar tus herramientas cuando el cliente poida diferentes tareas ",
)


message = agent.invoke(
    {"messages": [HumanMessage("quiero hacer un tweet de los pugs")]}
    )

dict_ifo = message["messages"][-1]    

parsed_result = parser.invoke(dict_ifo)

print(dict_ifo)
print(parsed_result)