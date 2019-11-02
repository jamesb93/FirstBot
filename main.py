import telegram
import requests
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from filters import _lidget, _thorncliffe, _southgate, _gym, _town

# tokens and api keys
APP_ID = "c93efe1b"
APP_KEY = "eb40d1dd2a7d00f50e830e7b80816501"
TOKEN = '1055417369:AAHc3TbfOyBN9KMbfx6QXv654odNkhAJPok'

codes = {
    'Lidget' : 450022757,
    'Thorncliffe' : 450024470,
    'Southgate' : 450017238,
    'Gym' : 450022495,
    'Town' : 450016800
}

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

lidget_filter = _lidget()
thorncliffe_filter = _thorncliffe()
southgate_filter = _southgate()
gym_filter = _gym()
town_filter = _town()

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Lidget", callback_data='lidget'),
        InlineKeyboardButton("Thorncliffe", callback_data='thorncliffe')],
        [InlineKeyboardButton("Southgate", callback_data='southgate'),
        InlineKeyboardButton("Town", callback_data='town')],
        [InlineKeyboardButton("Gym", callback_data='gym')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Choose a stop:', reply_markup=reply_markup)
    bot.send_message(
        chat_id=chat_id, 
        text="Custom Keyboard Test", 
        reply_markup=reply_markup
    )

def get_info(update, context):
    all_bus_info = ""
    stop = codes[update.message.text]
    timetable_request = f'http://transportapi.com/v3/uk/bus/stop/{stop}/live.json?&app_id={APP_ID}&app_key={APP_KEY}&group=no'
    r = requests.get(timetable_request)
    data = r.json()
    keys = [k for k in data.keys()]
    values = [v for v in data.values()]
    departures = data['departures']['all']
    for i in range(len(departures)):
        bus_info = departures[i]
        if bus_info['operator'] == 'FCH':
            route_number = bus_info['line']
            time = bus_info['best_departure_estimate']
            post = f'*{route_number}* - {time} \n'
            all_bus_info += post


    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=all_bus_info,
        parse_mode=telegram.ParseMode.MARKDOWN
    )

lidget_handler = MessageHandler(lidget_filter, get_info)
thorncliffe_handler = MessageHandler(thorncliffe_filter, get_info)
southgate_handler = MessageHandler(southgate_filter, get_info)
gym_handler = MessageHandler(gym_filter, get_info)
town_handler = MessageHandler(town_filter, get_info)

dispatcher.add_handler(lidget_handler)
dispatcher.add_handler(thorncliffe_handler)
dispatcher.add_handler(southgate_handler)
dispatcher.add_handler(gym_handler)
dispatcher.add_handler(town_handler)
updater.dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()