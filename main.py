import requests
import telegram
import time
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFILIADO = os.getenv("ML_AFFILIATE_CODE")
PALABRA_CLAVE = os.getenv("KEYWORD")
INTERVALO = int(os.getenv("INTERVAL"))  # en segundos

bot = telegram.Bot(token=TOKEN)

def buscar_productos(consulta):
    url = f'https://api.mercadolibre.com/sites/MLM/search?q={consulta}&limit=5'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()['results']
    return []

def publicar_productos():
    productos = buscar_productos(PALABRA_CLAVE)
    for producto in productos:
        titulo = producto['title']
        precio = producto['price']
        link = producto['permalink'] + AFILIADO
        mensaje = f"🛒 *{titulo}*\n💵 Precio: ${precio}\n🔗 [Ver producto]({link})"
        bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
        time.sleep(5)

while True:
    publicar_productos()
    time.sleep(INTERVALO)
