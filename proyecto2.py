from practicas2 import vector_store
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
#--------------------------------------------------
#importaciones para el agente que se aencarga de recibir la nformacion 
from langchain_openai import ChatOpenAI #este es para llamr al modelo del llm
from langchain_core.prompts import ChatPromptTemplate #este es el qeu se  encarga de darle las instrucciones al modelo
from langchain.chain.combine_documents import create_stuff_documents_chain # este se va a encargar de apsar todos los chunks que el modelo encuentre para darselos al  contexto del modelo
from langchain.cahin import create_retrieval_chain #recibe la informacion del retriver y la info de la cadena de documentos


load_dotenv()

loader = TextLoader("fizzbuzz.txt") #aqui tomamos la informacion que esta dentro del archvio txt
documents = loader.load() #aqui lo que hacemos es cargar esa informaacion que almacenamos en la variable anterior
                        #y la preparamos para que sea dividida po el chunkenizador 

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 100,chunk_overlap = 20) # aqui  con el divisro de texto nos encargamos de definir en cunatos caracteres se hara la division y de cuanto seara el overlap

chunks = text_splitter.split_documents(documents)# aqui nos encargamos de definir que documentovamos a chunkenizar
                                                #pasandle los aprametros que estan en la variable de text_splitter
                                                # y en el llamado ponermos el documento que habiamos cargado antes en la variable documents


mis_embedding = OpenAIEmbeddings() #esta es la herramienta que nos permite acceder a crear los ambeddings
vectorstore = FAISS.from_documents(chunks, mis_embedding)#aqui lo que ahcemos es guardar toda la informacon de nuestra empresa en embeddings 
print("base de datos creada exitosamente")

retriever = vectorstore.as_retriever() #aqui hacmos la extraccion de datos de esa base de datos del FAISS haciendo la comparacion vectorial