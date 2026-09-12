

import os
import random
import asyncio
import logging
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------------------------------------------------------------------------
# Configuración inicial
# ---------------------------------------------------------------------------
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Datos del grupo (EDITAR con la información real del grupo)
# ---------------------------------------------------------------------------
INTEGRANTES = [
    {"nombre": "Dennis Alexander Gamboa Stokes", "carnet": "201700747"},
]

CONTACTO = (
    "📧 Correo: dennis2441@gmail.com\n"
    "🌐 Repositorio: https://github.com/tu_usuario/tu_repositorio"
)

# ---------------------------------------------------------------------------
# Textos de ayuda (usados por /ayuda, /menu y validaciones)
# ---------------------------------------------------------------------------
AYUDA_TEXTO = (
    "📖 *Comandos disponibles:*\n\n"
    "/hola - Saluda al usuario por su nombre de Telegram.\n"
    "/hora - Muestra la fecha y hora actual.\n"
    "/contacto - Muestra la información de contacto del grupo.\n"
    "/integrantes - Muestra los integrantes del grupo (nombre y carnet).\n"
    "/ayuda - Muestra este mensaje de ayuda.\n"
    "/menu - Muestra un menú interactivo con botones.\n"
    "/calcular <num1> <operador> <num2> - Suma (+), resta (-), "
    "multiplica (*) o divide (/) dos números.\n"
    "    Ejemplo: /calcular 8 + 5\n"
    "/tabla <numero> - Muestra la tabla de multiplicar del 1 al 10.\n"
    "    Ejemplo: /tabla 7\n"
    "/convertir <cantidad> <origen> <destino> - Convierte unidades de "
    "longitud (cm, m, km, mi, ft).\n"
    "    Ejemplo: /convertir 10 km mi\n"
    "/aleatorio <min> <max> - Genera un número entero aleatorio en el rango dado.\n"
    "    Ejemplo: /aleatorio 1 100"
)

# Factores de conversión de cada unidad a metros
FACTORES_LONGITUD = {
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
    "ft": 0.3048,
}


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------
async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = update.effective_user
    nombre = usuario.first_name or usuario.username or "amigo/a"
    await update.message.reply_text(f"¡Hola, {nombre}! 👋 Bienvenido/a al bot de la Tarea #3.")


async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    await update.message.reply_text(f"🕒 Fecha y hora actual: {ahora}")


async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📇 *Información de contacto:*\n\n{CONTACTO}", parse_mode="Markdown")


async def integrantes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "\n".join(f"• {i['nombre']} - Carnet: {i['carnet']}" for i in INTEGRANTES)
    await update.message.reply_text(f"👥 *Integrantes del grupo:*\n\n{lista}", parse_mode="Markdown")


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(AYUDA_TEXTO, parse_mode="Markdown")


async def calcular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    uso = "⚠️ Uso correcto: /calcular <numero1> <operador> <numero2>\nOperadores válidos: + - * /\nEjemplo: /calcular 10 * 5"

    if len(args) != 3:
        await update.message.reply_text(uso)
        return

    num1_str, operador, num2_str = args

    try:
        num1 = float(num1_str)
        num2 = float(num2_str)
    except ValueError:
        await update.message.reply_text(
            "❌ Los valores ingresados no son números válidos.\n\n" + uso
        )
        return

    if operador not in ("+", "-", "*", "/"):
        await update.message.reply_text(
            f"❌ Operador '{operador}' no reconocido.\n\n" + uso
        )
        return

    if operador == "+":
        resultado = num1 + num2
    elif operador == "-":
        resultado = num1 - num2
    elif operador == "*":
        resultado = num1 * num2
    else:  # división
        if num2 == 0:
            await update.message.reply_text("❌ No es posible dividir entre cero.")
            return
        resultado = num1 / num2

    # Mostrar como entero si no tiene decimales
    if resultado == int(resultado):
        resultado = int(resultado)

    await update.message.reply_text(f"🧮 Resultado: {num1_str} {operador} {num2_str} = {resultado}")


async def tabla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    uso = "⚠️ Uso correcto: /tabla <numero>\nEjemplo: /tabla 7"

    if len(args) != 1:
        await update.message.reply_text(uso)
        return

    try:
        numero = float(args[0])
    except ValueError:
        await update.message.reply_text("❌ El valor ingresado no es un número válido.\n\n" + uso)
        return

    lineas = [f"{numero} x {i} = {numero * i}" for i in range(1, 11)]
    respuesta = f"✖️ *Tabla de multiplicar del {args[0]}:*\n\n" + "\n".join(lineas)
    await update.message.reply_text(respuesta, parse_mode="Markdown")


async def convertir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    uso = (
        "⚠️ Uso correcto: /convertir <cantidad> <unidad_origen> <unidad_destino>\n"
        "Unidades soportadas: cm, m, km, mi, ft\n"
        "Ejemplo: /convertir 10 km mi"
    )

    if len(args) != 3:
        await update.message.reply_text(uso)
        return

    cantidad_str, origen, destino = args
    origen = origen.lower()
    destino = destino.lower()

    try:
        cantidad = float(cantidad_str)
    except ValueError:
        await update.message.reply_text("❌ La cantidad ingresada no es un número válido.\n\n" + uso)
        return

    if origen not in FACTORES_LONGITUD or destino not in FACTORES_LONGITUD:
        await update.message.reply_text(
            f"❌ Unidad no soportada. Usa una de: {', '.join(FACTORES_LONGITUD.keys())}.\n\n" + uso
        )
        return

    metros = cantidad * FACTORES_LONGITUD[origen]
    resultado = metros / FACTORES_LONGITUD[destino]

    await update.message.reply_text(
        f"📏 {cantidad_str} {origen} = {round(resultado, 4)} {destino}"
    )


async def aleatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    uso = "⚠️ Uso correcto: /aleatorio <min> <max>\nEjemplo: /aleatorio 1 100"

    if len(args) != 2:
        await update.message.reply_text(uso)
        return

    try:
        minimo = int(args[0])
        maximo = int(args[1])
    except ValueError:
        await update.message.reply_text("❌ Los valores ingresados deben ser números enteros.\n\n" + uso)
        return

    if minimo > maximo:
        await update.message.reply_text("❌ El valor mínimo no puede ser mayor que el máximo.\n\n" + uso)
        return

    numero = random.randint(minimo, maximo)
    await update.message.reply_text(f"🎲 Número aleatorio entre {minimo} y {maximo}: {numero}")


# ---------------------------------------------------------------------------
# Menú interactivo
# ---------------------------------------------------------------------------
def construir_menu():
    teclado = [
        [InlineKeyboardButton("👋 Saludo", callback_data="menu_hola")],
        [InlineKeyboardButton("🕒 Hora", callback_data="menu_hora")],
        [InlineKeyboardButton("📇 Contacto", callback_data="menu_contacto")],
        [InlineKeyboardButton("👥 Integrantes", callback_data="menu_integrantes")],
        [InlineKeyboardButton("📖 Ayuda", callback_data="menu_ayuda")],
        [InlineKeyboardButton("🧮 Calculadora", callback_data="menu_calcular")],
        [InlineKeyboardButton("✖️ Tabla de multiplicar", callback_data="menu_tabla")],
        [InlineKeyboardButton("📏 Conversor de unidades", callback_data="menu_convertir")],
        [InlineKeyboardButton("🎲 Número aleatorio", callback_data="menu_aleatorio")],
    ]
    return InlineKeyboardMarkup(teclado)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *Menú interactivo:* elige una opción:",
        reply_markup=construir_menu(),
        parse_mode="Markdown",
    )


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    opcion = query.data

    if opcion == "menu_hola":
        usuario = query.from_user
        nombre = usuario.first_name or usuario.username or "amigo/a"
        texto = f"¡Hola, {nombre}! 👋 Bienvenido/a al bot de la Tarea #3."
    elif opcion == "menu_hora":
        texto = f"🕒 Fecha y hora actual: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    elif opcion == "menu_contacto":
        texto = f"📇 *Información de contacto:*\n\n{CONTACTO}"
    elif opcion == "menu_integrantes":
        lista = "\n".join(f"• {i['nombre']} - Carnet: {i['carnet']}" for i in INTEGRANTES)
        texto = f"👥 *Integrantes del grupo:*\n\n{lista}"
    elif opcion == "menu_ayuda":
        texto = AYUDA_TEXTO
    elif opcion == "menu_calcular":
        texto = "🧮 Usa: /calcular <numero1> <operador> <numero2>\nEjemplo: /calcular 10 * 5"
    elif opcion == "menu_tabla":
        texto = "✖️ Usa: /tabla <numero>\nEjemplo: /tabla 7"
    elif opcion == "menu_convertir":
        texto = "📏 Usa: /convertir <cantidad> <origen> <destino>\nUnidades: cm, m, km, mi, ft\nEjemplo: /convertir 10 km mi"
    elif opcion == "menu_aleatorio":
        texto = "🎲 Usa: /aleatorio <min> <max>\nEjemplo: /aleatorio 1 100"
    else:
        texto = "❌ Opción no reconocida."

    await query.edit_message_text(texto, reply_markup=construir_menu(), parse_mode="Markdown")


# ---------------------------------------------------------------------------
# Manejo de errores / comandos inexistentes
# ---------------------------------------------------------------------------
async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Comando no reconocido. Usa /ayuda para ver la lista de comandos disponibles."
    )


async def manejador_errores(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Ocurrió un error: %s", context.error)


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------
def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError(
            "No se encontró la variable de entorno TELEGRAM_TOKEN. "
            "Verifica tu archivo .env"
        )

    # Fix de compatibilidad con Python 3.13+/3.14: asyncio ya no crea
    # automáticamente un event loop en el hilo principal, así que lo
    # creamos manualmente antes de que la librería lo necesite.
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("hola", hola))
    app.add_handler(CommandHandler("hora", hora))
    app.add_handler(CommandHandler("contacto", contacto))
    app.add_handler(CommandHandler("integrantes", integrantes))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("calcular", calcular))
    app.add_handler(CommandHandler("tabla", tabla))
    app.add_handler(CommandHandler("convertir", convertir))
    app.add_handler(CommandHandler("aleatorio", aleatorio))

    # Botones del menú
    app.add_handler(CallbackQueryHandler(menu_callback))

    # Comandos no reconocidos
    app.add_handler(MessageHandler(filters.COMMAND, comando_desconocido))

    # Manejo global de errores
    app.add_error_handler(manejador_errores)

    logger.info("Bot iniciado. Esperando mensajes...")
    app.run_polling()


if __name__ == "__main__":
    main()