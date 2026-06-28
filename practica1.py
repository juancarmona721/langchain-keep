from pandas import describe_option
from dataclasses import field
from typing import Literal
from langchain_core import tools
import os
from dotenv import load_dotenv
load_dotenv()#aqui agregamos las variables dde entorno apra que el bot pueda hablar


# importamos los paquetes especificos  necesesarios para este proyecto
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from pydantic import BaseModel, Field   
from langchain.messages import HumanMessage
from typing import Literal


openai_api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    max_tokens=1500
)

class clasificador(BaseModel):
    """
    clasificacion de mensajes de los usuarios usando sus descripciones para saber como actuar sobre ellas
    """
    urgencia : str =Field(description= "clasificar la urgencia del mensaje del 1-5(urgencia = cosas criticas para la  conversacion)")
    tipo_mensaje: str = Field(description=" clasificar si el mensaje es: consulta, soporte tecnico o facturacion ")
    intervencion_humana: bool = Field(description=" revisar si el  mensaje necesita de la intervencion de un humano, True o false")

class clima(BaseModel):
    """
    buscar por queries de clima
    """
    ubicacion: str =  Field(description="nombre de la ciudad")
    unidad: Literal["celsius", "fahrenheit"] = Field(
        default= "celsius",
        description="preferencia de unidad de medida"
    )


@tool("clasificador_de_soporte", args_schema=clasificador)
def pregunta_normal(urgencia: str, tipo_mensaje: str, intervencion_humana: bool) -> object:
    """
    estas encargado de  clasificar tres aspectos del mensaaje de un cliente
    1. la urgencia
    2. clasificacion del mensaje(consulta, facturacion, soporte tecnico)
    3.requiere_humano(True, False)
    """
    return f"la urgencia del mensaje es: {urgencia}, el tipo de mensaje es:  {tipo_mensaje}, requiere intervencion?: {intervencion_humana}"


@tool("busca_el_clima_del_query", args_schema=clima)
def buscar_clima(ubicacion: str, unidad: str = "celsius") -> str:
    """
    obtener el clima actual y el pronostico
    """
    temp  = 22 if unidad == "celsius" else 72
    resultado = f"clima actual en {ubicacion}: {temp} grados {unidad[0].upper()}"
    return resultado



model_con_herramientas = model.bind_tools([pregunta_normal, buscar_clima])

mensaje_prueba = "Hola, mi internet no funciona y es muy urgente que me ayuden. Soporte técnico por favor"
respuesta = model_con_herramientas.invoke(mensaje_prueba)


print("Llamadas a herramientas detectadas:")
for tool_call in respuesta.tool_calls:
    print(f"Herramienta a usar: {tool_call['name']}")
    print(f"Argumentos extraídos: {tool_call['args']}")