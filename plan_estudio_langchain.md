# Mapa de Entrenamiento LangChain 2026 (Python)

Este mapa de entrenamiento está diseñado para desafiar tu lógica de programación. Cada proyecto se construye en un **único archivo de Python**, pero la complejidad y los conceptos introducidos en cada uno te servirán de base para el siguiente. 

La idea no es darte todo el código hecho, sino plantearte el reto, los conceptos clave y la estructura esperada para que tú investigues la implementación exacta utilizando las últimas versiones de LangChain (v0.3/v0.4+) y **LangGraph 1.0** (el hito de estabilidad de 2026).

## Proyecto 1: La Cadena Básica con LCEL
**Objetivo:** Familiarizarte con LangChain Expression Language (LCEL) y la interacción básica con un LLM.
*   **Reto:** Crea un script que reciba un tema por línea de comandos y genere un "tweet" divertido al respecto, devolviendo solo el texto del tweet sin comillas.
*   **Conceptos a investigar:** `ChatPromptTemplate`, inicialización de modelos (ej. `ChatOpenAI`), `StrOutputParser`, y cómo unirlos usando el operador pipe (`|`).
*   **Por qué sirve para el siguiente:** Entenderás cómo fluyen los datos (entradas -> prompt -> modelo -> salida). Esta es la base de todo.

## Proyecto 2: El Oráculo con Memoria (RAG Básico)
**Objetivo:** Introducir la Búsqueda y Generación Aumentada (RAG) pero manteniendo la sintaxis de LCEL.
*   **Reto:** Lee un archivo `.txt` local con información inventada (ej. "Reglas del juego de mesa FizzBuzz"). Crea una cadena que responda preguntas basándose **únicamente** en ese texto.
*   **Conceptos a investigar:** Document Loaders (`TextLoader`), Text Splitters (`RecursiveCharacterTextSplitter`), Embeddings, VectorStores (ej. `FAISS` o `Chroma`), y cómo crear un `Retriever`. 
*   **Por qué sirve para el siguiente:** Aprenderás a inyectar contexto externo al prompt del LLM, una habilidad crucial para darle "herramientas" de conocimiento al modelo.

## Proyecto 3: El Agente Autónomo con Herramientas Propias
**Objetivo:** Pasar de cadenas estáticas a un **Agente** que decide qué hacer basándose en herramientas que tú le programes.
*   **Reto:** Crea un agente que pueda responder a la pregunta: *"¿Cuál es la temperatura actual en X ciudad y cuánto es eso multiplicado por 5?"*.
*   **Conceptos a investigar:** El decorador `@tool` de `langchain_core.tools`, `create_tool_calling_agent`, `AgentExecutor`. Tendrás que crear dos herramientas de Python: una que finja buscar el clima y otra que multiplique números.
*   **Por qué sirve para el siguiente:** Entenderás el concepto de "Tool Calling" (llamada a herramientas). Un agente es simplemente un LLM tomando decisiones en un bucle hasta que resuelve el problema.

## Proyecto 4: Flujos de Trabajo Complejos y Subgrafos (LangGraph 1.0)
**Objetivo:** Migrar la lógica de agentes de LangChain (que es un poco caja negra) a **LangGraph**, aprovechando la orquestación avanzada de subgrafos.
*   **Reto:** Recrea el Proyecto 3, pero en lugar de usar `AgentExecutor`, construye un grafo (`StateGraph`) donde un nodo es el LLM y otro nodo ejecuta las herramientas. Intenta separar la lógica en dos submódulos (subgrafos) que se comuniquen entre sí.
*   **Conceptos a investigar:** `StateGraph`, `TypedDict` para definir el estado (State), Subgraph orchestration (novedad para dividir flujos), `END`, y gestión automática del estado duradero.
*   **Por qué sirve para el siguiente:** LangGraph te da control total sobre ciclos y estados. Esto te preparará para arquitecturas más avanzadas.

## Proyecto 5: El Supervisor con "Time-Travel" e Interrupciones en Vivo
**Objetivo:** Construir un flujo de producción resistente a fallas, aprovechando la interrupción de streaming y el "viaje en el tiempo" (Time-Travel) de LangGraph.
*   **Reto:** Crea un flujo en LangGraph que redacte un correo electrónico y tenga una herramienta para "enviarlo". Antes de que el nodo de envío se ejecute, el grafo debe pausarse, permitirte modificar el estado manualmente y continuar.
*   **Conceptos a investigar:** Persistencia automática, puntos de interrupción dinámicos, "Time-Travel" debugging, e integraciones de observabilidad con **LangSmith**.
*   **Resultado final:** Un entendimiento sólido de cómo construir sistemas de IA seguros y controlables para producción.
