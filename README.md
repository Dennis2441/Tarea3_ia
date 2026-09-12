# Tarea #3 - Bot de Telegram Interactivo

## Integrantes

| Nombre | Carnet |
|---|---|
| Dennis Alexander Gamboa Stokes | 201700747 |

## Descripción del bot

Bot de Telegram desarrollado en **Python** utilizando la librería `python-telegram-bot` y variables de entorno para el manejo seguro del token. Permite la interacción mediante comandos, recibe parámetros, valida entradas inválidas y cuenta con un menú interactivo basado en botones de Telegram.

## Instrucciones de instalación y ejecución

1. Clonar el repositorio y ubicarse en la carpeta `Tarea3`:
   ```bash
   cd Tarea3
   ```
2. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crear el bot en Telegram con **BotFather** y copiar el token generado.
5. Copiar `.env.example` a `.env` y colocar el token real:
   ```bash
   cp .env.example .env
   ```
   ```
   TELEGRAM_TOKEN=tu_token_real_aqui
   ```
6. Ejecutar el bot:
   ```bash
   python bot.py
   ```
7. Para mantenerlo disponible durante la evaluación, desplegar en un servicio en la nube (Railway, Render, un VPS, etc.) usando la misma variable de entorno `TELEGRAM_TOKEN`.

## Lista de comandos implementados

| Comando | Descripción |
|---|---|
| `/hola` | Saluda al usuario utilizando su nombre de Telegram. |
| `/hora` | Muestra la fecha y hora actual obtenida dinámicamente. |
| `/contacto` | Muestra la información de contacto definida por el grupo. |
| `/integrantes` | Muestra el nombre y carnet de los integrantes del grupo. |
| `/ayuda` | Muestra la lista de comandos disponibles con una breve descripción. |
| `/menu` | Muestra un menú interactivo mediante botones de Telegram. |
| `/calcular <numero1> <operador> <numero2>` | Realiza suma (+), resta (-), multiplicación (*) o división (/). |
| `/tabla <numero>` | Muestra la tabla de multiplicar del número indicado, del 1 al 10. |
| `/convertir <cantidad> <unidad_origen> <unidad_destino>` | Convierte unidades de longitud: cm, m, km, mi, ft. |
| `/aleatorio <min> <max>` | Genera un número entero aleatorio dentro del rango indicado. |

Todos los comandos que reciben parámetros validan la información ingresada. Si el comando no existe o los parámetros son inválidos o incompletos, el bot responde con un mensaje de error y muestra la forma correcta de utilizarlo.

## Detalle de la contribución de cada integrante

| Integrante | Parte de la tarea realizada |
|---|---|
| Dennis Alexander Gamboa Stokes | Desarrollo completo del bot: comandos (/hola, /hora, /contacto, /integrantes, /ayuda, /calcular, /tabla, /convertir, /aleatorio), menú interactivo, manejo de errores, despliegue y documentación. |
