import telebot
from datetime import datetime
from datetime import timedelta
from time import sleep
import time
from threading import Thread


bot = telebot.TeleBot("TOKEN")
mementos = []
chat_ids = {
    "log": "CHAT_ID"
}

"возвращает текущие дату и время"
def cur_time():
    res = '.'.join([time.strftime("%x").split('/')[1],
                    time.strftime("%x").split('/')[0],
                    time.strftime("%x").split('/')[2]])
    ans = res + ' ' + time.strftime('%X')
    # print(ans)
    return ans


"сверяет текущее время с первым напоминанием в списке"
def time_check(memo):
    while True:
        lim = reminder_preparation(cur_time())
        if memo[0] == lim[0] and memo[1][0] == lim[1][0] and memo[1][1] == lim[1][1]:
            bot.send_message(chat_id=memo[1][2], text=memo[2])
            break
        sleep(1)


"преобразует строку вида 'д.м.гггг' и её производные в единый формат 'дд.мм.гг'"
def dateparse(d_m_y):
    date = d_m_y.split('.')
    if len(date[0]) == 1:
        day = '0' + date[0]
    else:
        day = date[0]
    if len(date[1]) == 1:
        month = '0' + date[1]
    else:
        month = date[1]
    try:
        if len(date[2]) > 2:
            year = date[2][2:]
        else:
            year = date[2]
    except:
        year = str(datetime.now())[2:4]

    res_date = '.'.join([day, month, year])
    return res_date


"""убирает всё лишнее из мемо и преобразует его в список вида '[дата_время, текст мемо]', 
а также преобразует всякие 'сегодня' - 'завтра' в числовые даты через timedelta"""
def reminder_preparation(userinp):
    try:
        # print(f"\nreminder = {userinp}")
        rem = userinp.split()
        day_delta = 0
        if rem[1].lower() == 'в':
            del rem[1]
        if rem[0].lower() == "завтра":
            day_delta = 1
        elif rem[0].lower() == "послезавтра":
            day_delta = 2
        elif rem[0].lower() == "сегодня":
            day_delta = 0
        elif '.' in rem[0][0:4]:
            r_d = dateparse(rem[0]).split(".")
            for k in range(3):
                r_d[k] = int(r_d[k])

            r_t = [int(rem[1].split(":")[0]), int(rem[1].split(":")[1])]
            ans_txt = ' '.join(rem[2:])
            # print('\n', ans_dt, ans_txt, '\n')
            return [r_d, r_t, ans_txt]
        else:
            pass
        r_p_date = datetime.now() + timedelta(days=day_delta)
        r_d = str(r_p_date).split()[0].split('-')
        r_d.reverse()
        if len(r_d[2]) > 2:
            subst = r_d[2]
            r_d[2] = subst[2:]
        for i in range(3):
            r_d[i] = int(r_d[i])

        r_t = [int(rem[1].split(":")[0]), int(rem[1].split(":")[1])]
        ans_txt = ' '.join(rem[2:])
        return [r_d, r_t, ans_txt]
    except:
        return "RETRY"


"вставляет мемо на нужное место"
def insertion(memo, listo):
    if len(listo) == 0:
        listo.append(memo)
        return
    elif len(listo) == 1:
        nextr = listo[0]
        if memo[0][2] < nextr[0][2]:
            print("year")
            listo.insert(0, memo)
            return
        elif memo[0][2] == nextr[0][2] and \
                memo[0][1] < nextr[0][1]:
            print("month")
            listo.insert(0, memo)
            return
        elif memo[0][2] == nextr[0][2] and \
                memo[0][1] == nextr[0][1] and \
                memo[0][0] < nextr[0][0]:
            print("day")
            listo.insert(0, memo)
            return
        elif memo[0][2] == nextr[0][2] and \
                memo[0][1] == nextr[0][1] and \
                memo[0][0] == nextr[0][0] and \
                memo[1][0] < nextr[1][0]:
            print("hour")
            listo.insert(0, memo)
            return
        elif memo[0][2] == nextr[0][2] and \
                memo[0][1] == nextr[0][1] and \
                memo[0][0] == nextr[0][0] and \
                memo[1][0] == nextr[1][0] and \
                memo[1][1] < nextr[1][1]:
            print("minute")
            listo.insert(0, memo)
            return
        else:
            print("next")
            listo.append(memo)
            return
    for index in range(len(listo)):
        nextr = listo[index]
        if memo[0][2] < nextr[0][2]:
            print("year")
            listo.insert(index, memo)
            return
        elif memo[0][2] == nextr[0][2] and \
                memo[0][1] < nextr[0][1]:
            print("month")
            listo.insert(index, memo)
            return
        elif memo[0][2] == nextr[0][2] and \
                memo[0][1] == nextr[0][1] and \
                memo[0][0] < nextr[0][0]:
            print("day")
            listo.insert(index, memo)
            return
        elif memo[0][2] == nextr[0][2] and \
                memo[0][1] == nextr[0][1] and \
                memo[0][0] == nextr[0][0] and \
                memo[1][0] < nextr[1][0]:
            print("hour")
            listo.insert(index, memo)
            return
        elif memo[0][2] == nextr[0][2] and \
                memo[0][1] == nextr[0][1] and \
                memo[0][0] == nextr[0][0] and \
                memo[1][0] == nextr[1][0] and \
                memo[1][1] < nextr[1][1]:
            print("minute")
            listo.insert(index, memo)
            return
        elif index == len(listo) - 1:
            listo.append(memo)
            return
        else:
            print("next")

"подфункция, вычисляющая дату отправки"
def sent_datime():
    a = str(datetime.now()).split(':')
    dateandtime = (a[0] + ':' + a[1]).split()
    date = dateandtime[0].split('-')
    date.reverse()
    date = '.'.join(date)
    tim = dateandtime[1]
    return 'On:\n' + date + '\nAt:\n' + tim

"функция, сохраняющая информацию об отправке для логирования"
def get_sender_data(input_msg):
    sender = input_msg.split(',')
    sender_cats = []
    sender_data = []
    sender[0] = sender[0].replace("{", "")
    sender[-1] = sender[-1].replace("}", "")
    for i in range(len(sender)):
        sender[i] = sender[i].replace("'", "")
        sender[i] = sender[i].replace(" ", "")
        sender[i] = sender[i].split(":")
        sender_cats.append(sender[i][0])
        sender_data.append(sender[i][1])
    return ''.join(
        ["this msg was sent by:\n", sender_data[2], ' ', sender_data[1], "\nwhose username is:\n", sender_data[3], '\n']
    )


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет, меня пока допиливают,\
 но я уже готов помочь :)')


@bot.message_handler(commands=['help', 'info'])
def send_welcome(message):
    bot.reply_to(message, 'формат ввода напоминания\n\nчерез пробел:\n1) слова "нм" либо "напомни мне"'
                          '\n2) дата(дд.мм.гг)\n3) время(чч:мм)\n4) текст напоминания\n\n')


@bot.message_handler(func=lambda message: True)
def chat(message):
    def logo(msg):
        bot.send_message(chat_id=chat_ids["log"], text='"' + msg.text + '"' + "\n\n" +
                                                       get_sender_data(str(msg.chat)) + sent_datime())
    logo(message)

    if message.text.lower() == 'go offline':
        raise Exception("received a kill command")

    elif message.text.lower()[0:2] == 'нм':
        memo = " ".join(message.text.split()[1:])
        memo = reminder_preparation(memo)
        if memo == "RETRY":
            bot.reply_to(message, "несоответствие формату, используйте команду /help или повторите ввод")
            return
        memo[1].append(str(message.chat.id))
        # bot.send_message(chat_id=memo[1][2], text=memo[2])
        insertion(memo, mementos)
        bot.reply_to(message, "напоминание принято")

    elif message.text.lower()[0:11] == 'напомни мне':
        memo = " ".join(message.text.split()[2:])
        memo = reminder_preparation(memo)
        if memo == "RETRY":
            bot.reply_to(message, "несоответствие формату, используйте команду /help или повторите ввод")
            return
        memo[1].append(str(message.chat.id))
        # bot.send_message(chat_id=memo[1][2], text=memo[2])
        insertion(memo, mementos)
        bot.reply_to(message, "напоминание принято")

    else:
        bot.reply_to(message, "запрос не распознан, используйте команду /help или повторите ввод")

def interaction():
    if __name__ == '__main__':
        bot.polling(none_stop=True)

def remming():
    while True:
        try:
            time_check(mementos[0])
            del mementos[0]
        except:
            pass

t1 = Thread(target=interaction)
t2 = Thread(target=remming)

t1.start()
t2.start()
