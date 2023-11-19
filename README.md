
# Whatsapp Bot con Python
🚀El futuro donde las conversaciones con data suene tan natural como las conversaciones entre humanos, podrían no estar tan lejos! 😎🚀

Te invito a leer mi último artículo donde te muestro cómo integrar ChatGPT-4 con SQL usando Langchain y la API de WhatsApp Cloud, llevando los chatbots a un nuevo nivel de interacción de datos. 

#chatgpt4  #SQL #Langchain #openai  #WhatsAppCloudAPI #postgresql #DataIntegration #Chatbots #AI #InnovaciónTech #Tecnología #AprendizajeAutomático
https://www.linkedin.com/pulse/conversando-con-datos-integraci%2525C3%2525B3n-llm-sql-whatsapp-cloud-alvarez-rjcte%3FtrackingId=GzkvIYJiT7yU%252BZQjGfAKTw%253D%253D/?trackingId=GzkvIYJiT7yU%2BZQjGfAKTw%3D%3D

## Descarga el proyecto


```bash
git clone https://github.com/JPierr3/bigdateros-llm-sql.git
```




## Para probarlo localmente

1. Dirigete al directorio donde descargaste el proyecto

2. Crea un ambiente virtual con la version de python 3.10

```bash
  virtualenv -p 3.10.11 .venv
```
3. Activa el ambiente virtual

```bash
  source .venv/bin/activate
```
4. Instala las dependencias

```bash
  pip install -r requirements.txt
```

5. Corre el aplicativo

```bash
  python app.py
```


## Simular mensajes del usuario con postman

```javascript
Ingresar la URL
http://127.0.0.1:5000/webhook


en body, seleccionar "raw" y tipo "JSON", no olvidar agregar tu número
{
  "object": "whatsapp_business_account",
  "entry": [{
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [{
          "value": {
              "messaging_product": "whatsapp",
              "metadata": {
                  "display_phone_number": "PHONE_NUMBER",
                  "phone_number_id": "PHONE_NUMBER_ID"
              },
              "contacts": [{
                  "profile": {
                    "name": "NAME"
                  },
                  "wa_id": "PHONE_NUMBER"
                }],
              "messages": [{
                  "from": "agrega tu numero",
                  "id": "wamid.ID",
                  "timestamp": "1689257642",
                  "text": {
                    "body": "hola"
                  },
                  "type": "text"
                }]
          },
          "field": "messages"
        }]
  }]
}
```

## Consultas SQL 

```sql
-- 1. ¿Qué me recetaron en mi última cita?
SELECT medicamento, dosificacion
FROM recetas
WHERE cita_id = (
    SELECT MAX(cita_id)
    FROM citas
    WHERE paciente_id = (
        SELECT paciente_id
        FROM pacientes
        WHERE celular = '51937555915'
    )
)


-- 2. ¿Cuando fue mi última cita
SELECT MAX(fecha_cita) 
FROM citas 
WHERE paciente_id = (
    SELECT paciente_id 
    FROM pacientes 
    WHERE celular = '51937555915'
)

-- 3. ¿Cuantos días han pasado desde mi ultima cita ?
SELECT EXTRACT(DAY FROM NOW() - MAX(fecha_cita)) AS dias_desde_ultima_cita
FROM citas
WHERE paciente_id = (
    SELECT paciente_id
    FROM pacientes
    WHERE celular = '51937555915'
)








-- Creación de la tabla pacientes
CREATE TABLE pacientes (
    paciente_id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero TEXT,
    direccion TEXT,
    telefono TEXT,
    celular TEXT,
    correo_electronico TEXT UNIQUE,
    tipo_sangre TEXT,
    alergias TEXT
);

-- Creación de la tabla citas
CREATE TABLE citas (
    cita_id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(paciente_id) ON DELETE CASCADE,
    fecha_cita TIMESTAMP NOT NULL,
    motivo TEXT,
    notas TEXT,
    doctor TEXT NOT NULL
);

-- Creación de la tabla recetas
CREATE TABLE recetas (
    receta_id SERIAL PRIMARY KEY,
    cita_id INTEGER REFERENCES citas(cita_id) ON DELETE CASCADE,
    medicamento TEXT NOT NULL,
    dosificacion TEXT,
    duracion TEXT,
    instrucciones TEXT
);


INSERT INTO public.pacientes (nombre,fecha_nacimiento,genero,direccion,telefono,celular,correo_electronico,tipo_sangre,alergias) VALUES
	 ('Ana Sánchez','1985-04-16','Femenino','123 Calle Ficticia','5551234','5555678','ana.sanchez@email.com','O+','Ninguna'),
	 ('Juan Pérez','1990-01-01','Masculino','Calle Ficticia 123','555-1234','937555915','juan.perez@example.com','A+','Penicilina');


INSERT INTO public.citas (paciente_id,fecha_cita,motivo,notas,doctor) VALUES
 (1,'2022-10-31 10:00:00','Dolor de cabeza','Se recomienda descanso y evitar luces fuertes','Dr. Martínez'),
 (1,'2022-11-15 09:00:00','Control de hipertensión','Paciente estable, se recomienda continuar con el tratamiento actual','Dra. González'),
 (1,'2022-12-01 11:00:00','Revisión de la vista','Paciente refiere molestias al leer, prescribir lentes','Dr. Ruiz'),
 (1,'2023-01-20 08:30:00','Chequeo general','Paciente en buen estado general, actualizar vacunas','Dr. Herrera'),
 (2,'2022-11-25 10:00:00','Consulta de rutina','Paciente sana, se recomienda dieta balanceada','Dr. López'),
 (2,'2022-12-15 16:00:00','Dolor abdominal','Dolor posiblemente causado por estrés. Realizar más pruebas si persiste.','Dra. Martínez'),
 (2,'2023-01-10 14:30:00','Control de alergias','Alergias estacionales, prescribir antihistamínicos.','Dr. Ramírez');


INSERT INTO public.recetas (cita_id,medicamento,dosificacion,duracion,instrucciones) VALUES
	 (1,'Paracetamol','500mg','cada 8 horas por 3 días','Tomar después de comer'),
	 (2,'Losartán','50mg','30 días','Tomar una vez al día por la mañana'),
	 (3,'Lágrimas artificiales','Aplicar','Según sea necesario','Usar cuando sienta sequedad en los ojos'),
	 (4,'Vacuna contra la gripe','Una dosis','Anual','Aplicar una dosis intramuscular'),
	 (5,'Multivitamínicos','100mg','30 días','Tomar una tableta diaria por la mañana'),
	 (6,'Ibuprofeno','400mg','5 días','Tomar una tableta cada 8 horas'),
	 (7,'Cetirizina','10mg','Según sea necesario','Tomar una tableta cuando tenga síntomas de alergia');
```

