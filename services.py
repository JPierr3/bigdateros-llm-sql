# Importaciones y configuraciones
import requests
import sett
import json
import time
import re

from datetime import datetime


from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from sqlalchemy.exc import ProgrammingError
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SQLDatabase

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    else:
        text = 'mensaje no procesado'
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data


def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text,number, messageId, name, timestamp):
    text = text.lower() 
    list = []

    pg_uri = f"postgresql+psycopg2://{sett.username}:{sett.password}@{sett.host}:{sett.port}/{sett.mydatabase}"

    llm = ChatOpenAI(model_name="gpt-4", 
                    openai_api_key=sett.OPENAI_API_KEY, 
                    temperature=0, 
                    verbose=True)

    
    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)
    

    _DEFAULT_TEMPLATE = """
    Dada una pregunta de entrada, crea una consulta SQL utilizando el dialecto {dialect}. La consulta debe ser directa, sin errores de sintaxis, y lista para ejecutar en un gestor de base de datos. No uses bloques de código ni comillas triples para formatear la consulta. Usa comillas simples solo para cadenas de caracteres literales.
    Unicamente debes buscar información en base al celular del paciente proporcionado.

    Contexto:
    Pregunta: "f{input}"
    Numero: celular del paciente: numero
    Tablas disponibles: {table_info}

    Instrucciones:
    1. Escribe la consulta SQL sin ningún tipo de comillas o bloques de código como marco. 
    2. Utiliza nombres de tablas y columnas tal como se presentan en las tablas disponibles.
    3. Utiliza siempre el numero de celular del paciente para obtener la información.
    3. Para filtrar por nombre de paciente, utiliza la tabla 'pacientes' para buscar el ID correspondiente.


    -. no brindes información de pacientes diferentes al numero de consulta y agregués el numero de telefono como respuesta.
    -. En caso pregunten por un paciente en especifico, validar que el nombre pertenezca al numero proporcionado en la consulta, si no hacen match mencionar que es informacion privada.
    -. Genera la respuesta basada en el resultado esperado de la consulta SQL siempre y cuando devuelva al menos 1 registro.
    -  Si la consulta no devuelve registros, está vacio o null, none ,  no intentes inventar una respuesta, solo responde que no hay informacion disponible.
    -. no brindar información adicional que no haya sido solicitada en la pregunta inicial, ejemplo: si no pregunta por los datos de la duracion o instruccion no brindarla, responder lo mas consciso posible, no debes mencionar que se esta filtrando el numero internamente
    -. No incluir el telefono del paciente y el nombre.
    - no menciones que se esta ejecutando consultas sql y no agreges campos de la consulta sql como parte de la respuesta.
    - no inventes respuestas si la consulta sql no tieme resultados, por ejemplo si preguntan por la cantidad de dias, responder con un numero entero.

    [Respuesta aquí]
    """.strip()

    PROMPT = PromptTemplate( input_variables=["input", "table_info", "dialect" ],  template=_DEFAULT_TEMPLATE )

    db = SQLDatabase.from_uri(pg_uri)

    db_chain = SQLDatabaseChain.from_llm(
        llm,
        db,
        prompt=PROMPT,
        verbose=True,
        use_query_checker=True,
        return_intermediate_steps=True,
    )
    input_con_numero = f"Para el número de celular {number}, " + text

    response = db_chain({'query': input_con_numero } ) 
    
    try:
        if "hola" in text:
            textMessage = text_Message(number,"¡Hola! 👋 Bienvenido a Soporte Bigdateros. ¿Cómo podemos ayudarte hoy?")

            replyReaction = replyReaction_Message(number, messageId, "🫡")
            list.append(replyReaction)
            list.append(textMessage)
        else :
            response = db_chain({'query': input_con_numero } ) 
            data = text_Message(number,str( response["result"]))
            list.append(data)
        
    except (ProgrammingError, ValueError) as exc:
        print(f"Error: {exc}")

   
    print('1')
    for item in list:
        print('2')
        enviar_Mensaje_whatsapp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    else:
        return s
