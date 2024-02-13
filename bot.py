import telebot
import requests
import json
import datetime

with open('secure.json', 'r') as f:
    credentials = json.load(f)

TELEGRAM_BOT_TOKEN = credentials.get('TELEGRAM_BOT_TOKEN')
sellerkey = credentials.get('sellerkey')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def extract_arg(text):
    return text.split()[1:]

def format_duration(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    duration_string = ''
    if days > 0:
        duration_string += f"{days} days "
    if hours > 0:
        duration_string += f"{hours} hours "
    if minutes > 0:
        duration_string += f"{minutes} minutes "
    if seconds > 0:
        duration_string += f"{seconds} secondes"
    return duration_string

def format_date(timestamp):
    dt_object = datetime.datetime.fromtimestamp(int(timestamp))
    return dt_object.strftime('%d/%m/%Y à %H:%M:%S')

@bot.message_handler(commands=['create'])
def create_license(message):
    args = extract_arg(message.text)
    if len(args) != 2:
        bot.reply_to(message, "Invalid number of parameters. Please provide expiry in days AND amount of keys.")
        return

    expiry, amount = args

    payload = {
        'sellerkey': sellerkey,
        'type': 'add',
        'format': 'JSON',
        'expiry': expiry,
        'mask': '******-******-******',
        'amount': amount,
        'character': '2' 
    }

    response = requests.get('https://keyauth.win/api/seller/', params=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            keys = data.get('keys', [])
            if keys:
                reply_text = "License(s) created successfully:\n"
                for key in keys:
                    reply_text += f" - 🔑 Checker Leclerc {expiry} Jours : {key}\n"
                bot.reply_to(message, reply_text)
            else:
                key = data.get('key')
                bot.reply_to(message, f"License created successfully: \n - 🔑 Checker Leclerc {expiry} Jours : {key}")
        else:
            bot.reply_to(message, "Failed to create license. Please check your parameters and try again.")
    else:
        bot.reply_to(message, "Failed to create license. Please check your parameters and try again.")

@bot.message_handler(commands=['ban'])
def ban_license(message):
    args = extract_arg(message.text)
    if len(args) != 2:
        bot.reply_to(message, "Invalid number of parameters. Please provide the license key and reason.")
        return

    key, reason = args

    payload = {
        'sellerkey': sellerkey,
        'type': 'ban',
        'key': key,
        'reason': reason,
        'userToo': 'true'
    }

    response = requests.get('https://keyauth.win/api/seller/', params=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            bot.reply_to(message, "License banned successfully.")
        else:
            bot.reply_to(message, "Failed to ban license. Please check your parameters and try again.")
    else:
        bot.reply_to(message, "Failed to ban license. Please check your parameters and try again.")

@bot.message_handler(commands=['lookup'])
def lookup_license(message):
    args = extract_arg(message.text)
    if len(args) != 1:
        bot.reply_to(message, "Nombre invalide de paramètres. Veuillez fournir la clé de licence pour obtenir des informations.")
        return

    key = args[0]

    payload = {
        'sellerkey': sellerkey,
        'type': 'info',
        'key': key
    }

    response = requests.get('https://keyauth.win/api/seller/', params=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            duration = format_duration(int(data['duration']))
            status = data['status']
            level = data['level']
            created_by = data['createdby']
            used_by = data['usedby']
            creation_date = format_date(data['creationdate'])

            formatted_info = f"🕒 Duration: {duration}\n"
            formatted_info += f"🔒 Status: {status}\n"
            formatted_info += f"🔑 Level: {level}\n"
            formatted_info += f"👤 Created By: {created_by}\n"
            if status == "Used" and used_by:
                formatted_info += f"👥 Used By: {used_by}\n"
                formatted_info += f"📅 Used On: {format_date(data['usedon'])}\n"
            formatted_info += f"📅 Creation Date: {creation_date}\n"

            bot.reply_to(message, f"Lookup Completed Successfully 🔎\n\n{formatted_info}")
        else:
            bot.reply_to(message, "Impossible de récupérer les informations de licence. Veuillez vérifier vos paramètres et réessayer.")
    else:
        bot.reply_to(message, "Impossible de récupérer les informations de licence. Veuillez vérifier vos paramètres et réessayer.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "Invalid command. Please use /create, /ban, or /lookup commands.")

bot.polling()
