from telegram.ext import Updater, CommandHandler
from pycoingecko import CoinGeckoAPI

bot_token = "" #El token del bot que nos provee telegram cuando creamos  uno

updater = Updater(token= bot_token, use_context = True)
dispatcher =updater.dispatcher

cg = CoinGeckoAPI()

def start(update, context):
	"""
	Devuelve el primer nombre de la persona que interactua con el bot, para iniciar
	tipeamos /start
	"""
	chat_id = update.message.chat_id
	first_name = update.message.from_user.first_name
	msg = "Hola {} bienvenido a nuestro bot".format(first_name)
	context.bot.sendMessage(chat_id = chat_id,text = msg )

def argumentos(update, context):
	"""
	El usuario pasa la moneda que quiere consultar, el programa se conecta a la api de coingecko
	y le pide la moneda solicitada
	"""
	chat_id = update.message.chat_id
	args = context.args
	moneda = args[0]
	
	try:
		price = cg.get_price(ids=moneda, vs_currencies='usd') 
		valor = price.get(moneda)
		precio = valor.get('usd')
		mensage = "El valor de " + moneda + " es $" + str(precio)
	except:
		mensage="No encontre tu moneda"
	context.bot.sendMessage(chat_id = chat_id,text = mensage )

def sorprice(update,context):
	"""
	Envia un audio al usuario
	"""
	chat_id = update.message.chat_id

	with open('AUDIO_FILE', 'rb') as audio_file:
		context.bot.sendVoice(chat_id=chat_id,
        voice=audio_file,
        caption='Hola, te envio este audio, escuchalo!')

start_handler = CommandHandler('start', start)
precio_handler = CommandHandler('precio', argumentos)
sorprice_handler = CommandHandler('sorprice',sorprice)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(precio_handler)
dispatcher.add_handler(sorprice_handler)

updater.start_polling()
