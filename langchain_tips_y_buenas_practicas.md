# Tips y Buenas Prácticas en LangChain / LangGraph (2026)

Este documento contiene pautas esenciales para desarrollar con las últimas versiones de LangChain (v0.3+) y LangGraph 1.0 (estabilidad total de 2026). La idea es darte las bases para que sepas **qué** buscar.

## 1. Importaciones de Librerías (La Nueva Estructura)
LangChain se ha dividido en paquetes más pequeños para ser más rápido y seguro. Ya no se importa todo de `langchain`.
*   **`langchain_core`**: Contiene las abstracciones base. De aquí importarás `ChatPromptTemplate`, `BaseMessage`, `StrOutputParser` y el decorador `@tool`. También encontrarás nuevos *middlewares* introducidos este año.
*   **Paquetes de Integración**: Usa paquetes específicos para cada proveedor en lugar de `langchain_community` cuando sea posible. Por ejemplo:
    *   En lugar de `from langchain.chat_models import ChatOpenAI` ❌
    *   Usa `from langchain_openai import ChatOpenAI` ✅
*   **`langgraph`**: El paquete dedicado a flujos de trabajo cíclicos y agentes, ahora con gestión de estado duradero de forma automática por defecto en sus versiones 1.0+.

## 2. Creación de Herramientas (Tools)
Las herramientas son funciones que el LLM puede invocar. La mejor y más moderna forma de crearlas es usando el decorador `@tool`.

### El Decorador `@tool`
Convierte una función normal de Python en una herramienta de LangChain.
**Lo que debes investigar por tu cuenta:**
*   ¿Cómo se usa el *Docstring* (comentario de la función) en el decorador `@tool`? (Pista: el LLM lee ese docstring para saber cuándo usar la herramienta).
*   ¿Cómo usar **Pydantic** para definir los tipos de datos de entrada de la herramienta? Es vital tipar los argumentos (ej. `x: int, y: int`).

*Mini ejemplo conceptual:*
```python
from langchain_core.tools import tool

@tool
def multiplicar(a: int, b: int) -> int:
    """Multiplica dos números enteros. Útil cuando necesitas calcular el producto de dos cantidades."""
    return a * b
```

## 3. Estructuras de Datos y Conexiones (LCEL y LangGraph)
*   **LCEL (LangChain Expression Language):** Se basa en el operador pipe `|`. Todo en LCEL es un objeto `Runnable`. Debes entender cómo se pasan los diccionarios de entrada a través del `Prompt -> LLM -> Parser`.
*   **El "Estado" en LangGraph 1.0:** LangGraph usa un diccionario tipado (generalmente definido con `TypedDict` de Python) que fluye por todos los nodos del grafo. Cada nodo (función) recibe el Estado actual y devuelve un diccionario con las modificaciones a ese estado.
    *   *Novedad de 2026:* La **persistencia de estado ahora es automática/durable** por defecto en entornos de producción, y permite funciones de "Time-Travel" (rebobinar el estado del grafo a un punto anterior y continuar desde ahí).
    *   *Desafío:* Investiga cómo usar `Annotated` y `operator.add` para hacer que una clave del estado sea una lista que acumule mensajes.

## 4. Middlewares de Resiliencia y Seguridad (2026)
Investiga los nuevos componentes modulares añadidos en las últimas versiones:
*   **Model Retries:** Estrategias automáticas de *exponential backoff* integradas para llamadas a LLMs que fallan.
*   **Content Moderation:** Interceptores de entrada/salida para validar la seguridad del contenido (ej. antes de enviar los datos al LLM).

## 4. Tipos de Mensajes
Acostúmbrate a pensar en la conversación como una lista de objetos de mensajes específicos, no solo strings:
*   `SystemMessage`: Instrucciones generales.
*   `HumanMessage`: Lo que dice el usuario.
*   `AIMessage`: Lo que responde el modelo.
*   `ToolMessage`: El resultado que devuelve una herramienta después de ser ejecutada.

*Recordatorio: Este documento solo te muestra la puerta. Tu trabajo es entrar en la documentación oficial de LangChain y LangGraph para ver cómo se implementa el código real.*
