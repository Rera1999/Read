import telebot
from database import User, session

TOKEN = '6738622070:AAHUoREqWOslqh3rol3BekbgRKuWdwQZmQ8'
bot = telebot.TeleBot(TOKEN)


def admin_panel(message):
    if message.chat.id == 6023224495:  
        bot.send_message(message.chat.id, "مرحبا بك في لوحة التحكم. استخدم /add_points أو /deduct_points لتعديل نقاط المستخدم.")
    else:
        bot.send_message(message.chat.id, "ليس لديك وصول إلى هذا القسم.")


@bot.message_handler(commands=['add_points'])
def add_points(message):
    if message.chat.id == 6023224495:  
        try:
            _, user_id, points = message.text.split()
            user = session.query(User).filter_by(id=int(user_id)).first()
            if user:
                user.points += int(points)
                session.commit()
                bot.send_message(message.chat.id, f"تمت إضافة {points} نقاط بنجاح للمستخدم {user_id}.")
            else:
                bot.send_message(message.chat.id, f"المستخدم {user_id} غير موجود.")
        except ValueError:
            bot.send_message(message.chat.id, "تنسيق غير صحيح. استخدم: /add_points <user_id> <points>")
    else:
        bot.send_message(message.chat.id, "ليس لديك وصول إلى هذا الأمر.")


@bot.message_handler(commands=['deduct_points'])
def deduct_points(message):
    if message.chat.id == 6023224495:  # تأكيد أن المستخدم هو الأدمن
        try:
            _, user_id, points = message.text.split()
            user = session.query(User).filter_by(id=int(user_id)).first()
            if user:
                user.points -= int(points)
                if user.points < 0:
                    user.points = 0
                session.commit()
                bot.send_message(message.chat.id, f"تمت خصم {points} نقاط بنجاح من المستخدم {user_id}.")
            else:
                bot.send_message(message.chat.id, f"المستخدم {user_id} غير موجود.")
        except ValueError:
            bot.send_message(message.chat.id, "تنسيق غير صحيح. استخدم: /deduct_points <user_id> <points>")
    else:
        bot.send_message(message.chat.id, "ليس لديك وصول إلى هذا الأمر.")


@bot.message_handler(commands=['id'])
def get_user_id(message):
    user_id = message.chat.id
    bot.send_message(message.chat.id, f"معرف المستخدم الخاص بك هو: {user_id}")


