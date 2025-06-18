import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from faker import Faker

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
fake = Faker()

def start(update, context):
    update.message.reply_text("👋 ¡Hola! Usa /gen seguido del código de país (ej. /gen mx)")

def generar_direccion(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Debes indicar un código de país. Ejemplo: /gen mx")
        return
    
    codigo = context.args[0].lower()
    try:
        fake_local = Faker(codigo)
        datos = {
            "nombre": fake_local.name(),
            "direccion": fake_local.address().replace("\n", ", "),
            "ciudad": fake_local.city(),
            "codigo_postal": fake_local.postcode(),
            "telefono": fake_local.phone_number(),
            "pais": codigo.upper()
        }

        mensaje = (
            f"👤 Nombre: {datos['nombre']}\n"
            f"🏠 Dirección: {datos['direccion']}\n"
            f"📍 Ciudad: {datos['ciudad']}\n"
            f"📫 Código Postal: {datos['codigo_postal']}\n"
            f"📞 Teléfono: {datos['telefono']}\n"
            f"🌍 País: {datos['pais']}"
        )
        update.message.reply_text(mensaje)
    except Exception:
        update.message.reply_text("Código de país no válido o no soportado.")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gen", generar_direccion))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
