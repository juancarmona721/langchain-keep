import sys
from dotenv import load_dotenv
# Importaciones clave de LangChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Cargamos tus variables de entorno (.env) para que funcione tu API Key de OpenAI
load_dotenv()


template = ChatPromptTemplate.from_messages([
    ("system", "Eres un comediante experto en Twitter. Debes escribir un tweet muy chistoso sobre el tema que te den. No uses comillas, solo devuelve el texto del tweet"),
    ("human", "Escribe un tweet sobre: {tema}")
])


modelo = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

cadena = template | modelo | parser



if len(sys.argv) < 2:
    print("debes escribir un tema. ejemplo: python proyecto_lcel.py pugs")
    sys.exit(1)

tema_elegido = sys.argv[1]

resultado = cadena.invoke({"tema": tema_elegido})

print(resultado)