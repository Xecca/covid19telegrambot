import COVID19Py
import telebot
from telebot import types
import flags

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot('myAPI')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Во всём мире')
    btn2 = types.KeyboardButton('Украина')
    btn3 = types.KeyboardButton('Россия')
    btn4 = types.KeyboardButton('Беларусь')
    markup.add(btn1, btn2, btn3, btn4)

    send_message = f"<b>Привет {message.from_user.first_name}!</b>\nЧтобы получить актуальные данные по количеству заболевших коронавирусом (COVID-19), напишите название страны, например: Россия, США, Украина, Spain, brazil и так далее\n\nБот находится в бета-тесте, поэтому подписывайся на канал и следи за обновлениями @coder_dreik_public"
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['refresh'])
def refresh(message):
    
    rank = covid19.getAll()
    countries_rank = {}

    for x in rank['locations']:
        # print(x['country_code'], x['country'], x['latest']['confirmed'], x['latest']['deaths'], x['latest']['recovered'])
        country_name = x['country']
        if (countries_rank.get(x['country']) == None):
            countries_rank.update({x['country']: x['latest'][message]})
        else:
            value = countries_rank.get(x['country'])
            countries_rank.update({x['country']: x['latest'][message] + value})
    print(countries_rank)

    return countries_rank
    # print(rank['locations'][1]['country_code'], rank['locations'][1]['latest']['confirmed'])

countries_rank_conf = refresh('confirmed')
countries_rank_deaths = refresh('deaths')
countries_rank_recovered = refresh('recovered')

# Функция, что сработает при отправке какого-либо текста боту
# Здесь мы создаем отслеживания данных и вывод статистики по определенной стране
@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    flag = ""
    get_message_bot = message.text.strip().lower()
    try:
        if get_message_bot == "сша" or get_message_bot == "usa":
            location = covid19.getLocationByCountryCode("US")
            flag = flags.country['United States']
        elif get_message_bot == "россия" or get_message_bot == "rus" or get_message_bot == "russia":
            location = covid19.getLocationByCountryCode("RU")
            flag = flags.country['Russia']
        elif get_message_bot == "узбекистан" or get_message_bot == "uzbekistan":
            location = covid19.getLocationByCountryCode("UA")
            flag = flags.country['Uzbekistan']
        elif get_message_bot == "украина" or get_message_bot == "ukraine":
            location = covid19.getLocationByCountryCode("UA")
            flag = flags.country['Ukraine']
        elif get_message_bot == "беларусь" or get_message_bot == "belarus" or get_message_bot == "белоруссия":
            location = covid19.getLocationByCountryCode("BY")
            flag = flags.country['Belarus']
        elif get_message_bot == "бразилия" or get_message_bot == "brazil" or get_message_bot == "белоруссия":
            location = covid19.getLocationByCountryCode("BR")
            flag = flags.country['Brazil']
        elif get_message_bot == "китай" or get_message_bot == "china":
            location = covid19.getLocationByCountryCode("CN")
            flag = flags.country['China']
        elif get_message_bot == "казакхстан" or get_message_bot == "kazakhstan":
            location = covid19.getLocationByCountryCode("KZ")
            flag = flags.country['Kazakhstan']
        elif get_message_bot == "киргизия" or get_message_bot == "kyrgyzstan":
            location = covid19.getLocationByCountryCode("KG")
            flag = flags.country['Kyrgyzstan']
        elif get_message_bot == "италия" or get_message_bot == "italy" or get_message_bot == "italia":
            location = covid19.getLocationByCountryCode("IT")
            flag = flags.country['Italy']
        elif get_message_bot == "франция" or get_message_bot == "france":
            location = covid19.getLocationByCountryCode("FR")
            flag = flags.country['France']
        elif get_message_bot == "германия" or get_message_bot == "germany":
            location = covid19.getLocationByCountryCode("DE")
            flag = flags.country['Germany']
        elif get_message_bot == "япония" or get_message_bot == "japan":
            location = covid19.getLocationByCountryCode("JP")
            flag = flags.country['Japan']
        elif get_message_bot == "испания" or get_message_bot == "spain":
            location = covid19.getLocationByCountryCode("ES")
            flag = flags.country['Spain']
        elif get_message_bot == "иран" or get_message_bot == "iran":
            location = covid19.getLocationByCountryCode("IR")
            flag = flags.country['Iran']
        else:
            location = covid19.getLatest()
            final_message = f"<u>Данные по всему миру </u>🌏\n<b>Заболевших: </b>" \
                f"{location['confirmed']:,} человек. 😷\n" \
                f"<b>Смертей: </b>{location['deaths']:,} ⚰️"

        if final_message == "":
            changes = covid19.getLatestChanges()
            date = location[0]['last_updated'].split("T")
            time = date[1].split(".")
            population = location[0]['country_population']
            # deaths = location[0]['latest']['deaths']
            deaths = countries_rank_deaths[location[0]['country']]
            # confirmed = location[0]['latest']['confirmed']
            confirmed = countries_rank_conf[location[0]['country']]
            # recovered = location[0]['latest']['recovered']
            recovered = countries_rank_recovered[location[0]['country']]
            confirmed_last = changes['confirmed']
            percent_confirmed_of_population = (confirmed / population) * 100
            final_message = f"<u>Данные по стране:</u> {flag}\n" \
                f"Население: {population:,} человек.\n" \
                f"<i>Последнее обновление:</i> {date[0]} {time[0]}\n" \
                f"⚡️Последние данные⚡️:\n<b>Заболевших: </b>{confirmed:,} 😷 \t ({round(percent_confirmed_of_population, 5):,} % от населения).\n" \
                f"<b>Смертей: </b>{deaths:,} ⚰️\n" \
                f"Выздоровело: {recovered:,}\n"
                # f"Заболевшие за последний день: {confirmed_last:,}"

        bot.send_message(message.chat.id, final_message, parse_mode='html')
    except Exception as e:
        print(e.__class__)
        # error_message = "В настоящее время сайт с данными недоступен. Попробуйте позже!"
        # bot.send_message(message.chat.id, error_message, parse_mode='html')
# Это нужно чтобы бот работал всё время
bot.polling(none_stop=True)
# latest = covid19.getLatest()
# location = covid19.getLocationByCountryCode("US")

# print(latest)
# print(location)
