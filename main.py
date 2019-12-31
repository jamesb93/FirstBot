import telegram, os, requests, datetime, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from filters import _lidget, _thorncliffe, _southgate, _gym, _town

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# tokens and api keys
APP_ID = os.environ.get("TRANSPORT_API_ID")
APP_KEY = os.environ.get("TRANSPORT_API_KEY")
TOKEN = os.environ.get("FIRST_BOT_TOKEN")

codes = {
    'Lidget' : 450022757,
    'Thorncliffe' : 450024470,
    'Southgate' : 450017238,
    'Gym' : 450022495,
    'Town' : 450016800
}

bus_operators = [
    'FHUD',
    'FCH',
    'FWYO'
]

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
    departures = data['departures']['all']
    if len(departures) == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_NO BUSES_",
            parse_mode=telegram.ParseMode.MARKDOWN
        )

    for i in range(len(departures)):
        bus_info = departures[i]
        if bus_info['operator'] in bus_operators:
            route_number = bus_info['line']
            time = bus_info['best_departure_estimate']
            post = f'*{route_number}* - {time} \n'
            all_bus_info += post

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=all_bus_info,
        parse_mode=telegram.ParseMode.MARKDOWN
    )

lidget_handler       = MessageHandler(lidget_filter, get_info)
thorncliffe_handler  = MessageHandler(thorncliffe_filter, get_info)
southgate_handler    = MessageHandler(southgate_filter, get_info)
gym_handler          = MessageHandler(gym_filter, get_info)
town_handler         = MessageHandler(town_filter, get_info)

dispatcher.add_handler(lidget_handler)
dispatcher.add_handler(thorncliffe_handler)
dispatcher.add_handler(southgate_handler)
dispatcher.add_handler(gym_handler)
dispatcher.add_handler(town_handler)
updater.dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()