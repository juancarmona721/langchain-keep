from langchain_openai import OpenAIEmbeddings #importamos los recurssos que vamos a utilizar para hacer el proceso de embeddings
from langchain_postgres import PGVector   #este es para poder establecer la conexion con nuestra base de datos de postgres
from getpass import getpass #???
import getpass
import os
from dotenv import load_dotenv

## aqui importamos los recursos que necesitmaso para darle un maneo a el texto q ue vamos a ingresar
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


vector_store = PGVector(
    embeddings=embeddings,
    collection_name="mis_documentos",
    connection="postgresql://postgres:Juanchito0721!/@db.coqhwbeqercrrtynvsuy.supabase.co:5432/postgres"
)

#empezamos a cargar el archivo que vamos  aanadir a nuestra  base de datos
loader = TextLoader("rag.txt")
documentos = loader.load()

#dividimos el texto en fragmentos que son los chunks para que la ia procese mejor esta informacion
text_splitter = RecursiveCharacterTextSplitter(chunk_size=400,
chunk_overlap=100)

fragmentos = text_splitter.split_documents(documentos)#subimos la informacion chunkeada a documentos, que es el que se encarga de tener disponible la inforamcion que queremos subir lista para cargarla a la  abse de datos

vector_store.add_documents(documentos) # traemos la informacion de conexion de las base de datos
print("se guaradron los documentos")



#=================================================================
# aqui vamos a establecer la conexion para que le  bot recupere la informacion

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


retriever = vector_store.as_retriever(search_kwargs={"k": 5})#este sse encarga de trae r los 3 fragmentos mas relevantesd de la base de datos

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) ### creamos el modelo que va a leer estas interacciones

template = """responder a la pregunta basandote UNICAMENTE en el siguientes contexto: 
contexto: {context}

pregunta: {question}
"""

prompt = ChatPromptTemplate.from_template(template)


def format_docs(docs): ### aqui lo que hacemos es juntar los fragmentos que se extrageron de la base de datos 
    return "\n\n".join(doc.page_content for doc in docs) 



rag_chain = (
    {"context": retriever | format_docs, "question":
    RunnablePassthrough()}
    |prompt
    |llm
    |StrOutputParser()
)

pregunta = "ahora que estoy usandote como rag, neceisto que me aydues a ejecutar un query sql en mi sql editor de supabase  para evitar que cada vez que ejecute el codigo se guarde nuevamente lainormacion que ya esat recopilada en el archivo rag.txt"
respuesta= rag_chain.invoke(pregunta)

print("respuesta", respuesta)
