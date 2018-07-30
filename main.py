import appsettings
import telebot
import srcrydata
import os
bot = telebot.TeleBot(appsettings.token)


@bot.message_handler(commands=["info"])
def infomsg(message):
    bot.send_message(message.chat.id, appsettings.info)


@bot.message_handler(commands=["help", "start"])
def getcmdlist(message):
    bot.send_message(message.chat.id, srcrydata.getcmdlist(message.chat.id))


@bot.message_handler(commands=["admins"])
def getadmins(message):
    if srcrydata.isop(message.chat.id):
        res = "Admins' IDs:\n"
        for op in srcrydata.getops():
            res += op + "\n"
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, appsettings.noperms)


@bot.message_handler(commands=["promote"])
def promote(message):
    if srcrydata.isop(message.chat.id):
        if len(message.text) < 10:
            bot.send_message(message.chat.id, appsettings.invalargs)
        else:
            topromote = message.text.split()[1]
            if srcrydata.isop(topromote):
                bot.send_message(message.chat.id, appsettings.alreadymod)
            else:
                srcrydata.addop(topromote)
                bot.send_message(message.chat.id, "User " + str(topromote) + " is promoted!")
    else:
        bot.send_message(message.chat.id, appsettings.noperms)


@bot.message_handler(commands=["downgrade"])
def downgrate(message):
    if srcrydata.isop(message.chat.id):
        if len(message.text) < 12:
            bot.send_message(message.chat.id, appsettings.invalargs)
        else:
            todowngrade = message.text.split()[1]
            if not srcrydata.isop(todowngrade):
                bot.send_message(message.chat.id, appsettings.notmod)
            else:
                srcrydata.removeop(todowngrade)
                bot.send_message(message.chat.id, "User " + str(todowngrade) + " is downgraded!")
    else:
        bot.send_message(message.chat.id, appsettings.noperms)


@bot.message_handler(commands=["generate"])
def genprom(message):
    if srcrydata.isop(message.chat.id):
        if len(message.text) < 11:
            bot.send_message(message.chat.id, appsettings.invalargs)
        else:
            params = message.text.split()
            if len(params) == 3:
                msg = "New promocodes:\n"
                num = int(params[2])
                i = 0
                while i < num:
                    msg += srcrydata.promgen(params[1]) + '\n'
                    i += 1
                bot.send_message(message.chat.id, msg)
            else:
                bot.send_message(message.chat.id, appsettings.invalargs)
    else:
        bot.send_message(message.chat.id, appsettings.noperms)


@bot.message_handler(commands=["getpromos"])
def getpromos(message):
    if srcrydata.isop(message.chat.id):
        msg = "Promocodes:\n"
        for pr in srcrydata.getpromos():
            msg += pr + "\n"
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, appsettings.noperms)


@bot.message_handler(commands=["getexp"])
def getpromos(message):
    if srcrydata.isop(message.chat.id):
        msg = "Expired promocodes:\n"
        for pr in srcrydata.getexpired():
            msg += pr + "\n"
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, appsettings.noperms)


@bot.message_handler(commands=["activate"])
def activate(message):
    if len(message.text) < 11:
        bot.send_message(message.chat.id, appsettings.invalargs)
    else:
        proms = srcrydata.getpromos()
        found = False
        for prom in proms:
            if message.text[10:] == prom[0:9]:
                found = True
                tick = False
                for expir in srcrydata.getexpired():
                    if message.text[10:] == expir:
                        tick = True
                        break
                if not tick:
                    bot.send_message(message.chat.id, appsettings.activated)
                    srcrydata.load(prom[9:])
                    bot.send_chat_action(message.chat.id, 'upload_document')
                    localname = appsettings.cache + "\\" + prom[9:].split('/')[-1]
                    bot.send_chat_action(message.chat.id, 'upload_document')
                    bot.send_document(message.chat.id, open(localname, 'rb'))
                    srcrydata.addexp(message.text[10:])
                    os.remove(localname)
                else:
                    bot.send_message(message.chat.id, appsettings.isexpired)
                break
        if not found:
            bot.send_message(message.chat.id, appsettings.notfound)


@bot.message_handler(commands=["id"])
def getid(message):
   bot.send_message(message.chat.id, str(message.chat.id))


if __name__ == '__main__':
    srcrydata.initcomps()
    bot.infinity_polling(True)
