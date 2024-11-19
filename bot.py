import telebot
from telebot import types
from database import User, session
from admin_panel import admin_panel

TOKEN = '6738622070:AAHUoREqWOslqh3rol3BekbgRKuWdwQZmQ8'
bot = telebot.TeleBot(TOKEN)

translations = {
    'english': {
        'welcome': "Welcome to the bot! Please select your language:",
        'language_set': "Language set to English",
        'collect_button': "Click to Collect Points",
        'upgrade_button': "Upgrade Collection Level",
        'admin_button': "Admin Panel",
        'contact_button': "Contact Admin",
        'complaint_button': "Submit Complaint",
        'start_using': "You can now start using the bot. Choose an option:",
        'points': "You have {points} points and are at level {level}!",
        'upgrade_successful': "You have successfully upgraded to level {level}!",
        'not_enough_points': "You don't have enough points to upgrade. You need {needed_points} more points.",
        'contact_message': "Please send your message, and I will forward it to the admin.",
        'message_sent': "Your message has been sent to the admin.",
        'enter_complaint': "Please enter your complaint:",
        'complaint_recorded': "Your complaint has been recorded."
    },
    'arabic': {
        'welcome': "مرحبًا بك في البوت! يرجى اختيار لغتك:",
        'language_set': "تم تعيين اللغة إلى العربية",
        'collect_button': "اضغط لتجميع النقاط",
        'upgrade_button': "ترقية مستوى التجميع",
        'admin_button': "لوحة التحكم",
        'contact_button': "تواصل مع الأدمن",
        'complaint_button': "تقديم شكوى",
        'start_using': "يمكنك الآن بدء استخدام البوت. اختر خيارًا:",
        'points': "لديك {points} نقاط وأنت في المستوى {level}!",
        'upgrade_successful': "لقد قمت بالترقية بنجاح إلى المستوى {level}!",
        'not_enough_points': "ليس لديك نقاط كافية للترقية. تحتاج إلى {needed_points} نقطة إضافية.",
        'contact_message': "يرجى إرسال رسالتك، وسوف أقوم بإرسالها إلى الأدمن.",
        'message_sent': "تم إرسال رسالتك إلى الأدمن.",
        'enter_complaint': "يرجى إدخال شكواك:",
        'complaint_recorded': "تم تسجيل شكواك."
    },
    'russian': {
        'welcome': "Добро пожаловать в бот! Пожалуйста, выберите ваш язык:",
        'language_set': "Язык установлен на русский",
        'collect_button': "Нажмите, чтобы собрать очки",
        'upgrade_button': "Улучшить уровень сбора",
        'admin_button': "Панель администратора",
        'contact_button': "Связаться с админом",
        'complaint_button': "Подать жалобу",
        'start_using': "Теперь вы можете начать использовать бота. Выберите опцию:",
        'points': "У вас {points} очков и вы на уровне {level}!",
        'upgrade_successful': "Вы успешно повысили уровень до {level}!",
        'not_enough_points': "У вас недостаточно очков для повышения уровня. Вам нужно еще {needed_points} очков.",
        'contact_message': "Пожалуйста, отправьте ваше сообщение, и я передам его админу.",
        'message_sent': "Ваше сообщение было отправлено админу.",
        'enter_complaint': "Пожалуйста, введите вашу жалобу:",
        'complaint_recorded': "Ваша жалоба была записана."
    },
    'spanish': {
        'welcome': "¡Bienvenido al bot! Por favor selecciona tu idioma:",
        'language_set': "Idioma configurado en español",
        'collect_button': "Haz clic para acumular puntos",
        'upgrade_button': "Mejorar nivel de colección",
        'admin_button': "Panel de administrador",
        'contact_button': "Contactar al administrador",
        'complaint_button': "Enviar una queja",
        'start_using': "Ahora puedes comenzar a usar el bot. Elige una opción:",
        'points': "¡Tienes {points} puntos y estás en el nivel {level}!",
        'upgrade_successful': "¡Has mejorado con éxito al nivel {level}!",
        'not_enough_points': "No tienes suficientes puntos para mejorar. Necesitas {needed_points} puntos más.",
        'contact_message': "Por favor, envía tu mensaje, y se lo haré llegar al administrador.",
        'message_sent': "Tu mensaje ha sido enviado al administrador.",
        'enter_complaint': "Por favor, introduce tu queja:",
        'complaint_recorded': "Tu queja ha sido registrada."
    }
}

levels = [100, 1000, 10000, 50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 12800000, 25600000, 51200000, 102400000]

def get_translation(chat_id, key):
    user = session.query(User).filter_by(id=chat_id).first()
    if user and user.language in translations:
        return translations[user.language][key]
    return translations['english'][key]  

def update_user_level(user):
    for i, level_threshold in enumerate(levels):
        if user.points < level_threshold:
            user.level = i + 1
            break
    else:
        user.level = len(levels)  

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    langs = ['English', 'Arabic', 'Russian', 'Spanish']
    for lang in langs:
        markup.add(types.InlineKeyboardButton(lang, callback_data=f"lang_{lang.lower()}"))

    bot.send_message(message.chat.id, get_translation(message.chat.id, 'welcome'), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    user = session.query(User).filter_by(id=call.message.chat.id).first()
    if user:
        user.language = lang
        session.commit()
    else:
        new_user = User(id=call.message.chat.id, language=lang, level=1, points=0)  
        session.add(new_user)
        session.commit()

   
    bot.send_message(call.message.chat.id, get_translation(call.message.chat.id, 'language_set'))
    show_main_menu(call.message)

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    collect_button = types.KeyboardButton(get_translation(message.chat.id, 'collect_button'))
    markup.add(collect_button)

    upgrade_button = types.KeyboardButton(get_translation(message.chat.id, 'upgrade_button'))
    markup.add(upgrade_button)
    
    
    if message.chat.id == 6023224495:
        admin_button = types.KeyboardButton(get_translation(message.chat.id, 'admin_button'))
        markup.add(admin_button)
    
    
    contact_button = types.KeyboardButton(get_translation(message.chat.id, 'contact_button'))
    markup.add(contact_button)
    
    
    complaint_button = types.KeyboardButton(get_translation(message.chat.id, 'complaint_button'))
    markup.add(complaint_button)
    
    bot.send_message(message.chat.id, get_translation(message.chat.id, 'start_using'), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == get_translation(message.chat.id, 'collect_button'))
def click_button(message):
    user = session.query(User).filter_by(id=message.chat.id).first()
    if user:
        user.points += 1 * user.level  
        update_user_level(user)
        session.commit()
        bot.send_message(message.chat.id, get_translation(message.chat.id, 'points').format(points=user.points, level=user.level))
    else:
        bot.send_message(message.chat.id, "Please set your language first using /start")

@bot.message_handler(func=lambda message: message.text == get_translation(message.chat.id, 'upgrade_button'))
def upgrade_button(message):
    user = session.query(User).filter_by(id=message.chat.id).first()
    if user:
        next_level = user.level + 1
        if next_level <= len(levels):
            needed_points = levels[next_level - 1] - levels[user.level - 1]  
            if user.points >= needed_points:
                user.points -= needed_points 
                user.level = next_level  
                session.commit()
                bot.send_message(message.chat.id, get_translation(message.chat.id, 'upgrade_successful').format(level=user.level))
            else:
                bot.send_message(message.chat.id, get_translation(message.chat.id, 'not_enough_points').format(needed_points=needed_points))
        else:
            bot.send_message(message.chat.id, "You have reached the maximum level.")
    else:
        bot.send_message(message.chat.id, "Please set your language first using /start")


@bot.message_handler(func=lambda message: message.text == get_translation(message.chat.id, 'admin_button'))
def admin(message):
    admin_panel(message)


@bot.message_handler(func=lambda message: message.text == get_translation(message.chat.id, 'contact_button'))
def contact_admin(message):
    bot.send_message(message.chat.id, get_translation(message.chat.id, 'contact_message'))
    bot.register_next_step_handler(message, forward_to_admin)

def forward_to_admin(message):
    bot.send_message(6023224495, f"Message from {message.chat.username}: {message.text}")
    bot.send_message(message.chat.id, get_translation(message.chat.id, 'message_sent'))

@bot.message_handler(func=lambda message: message.text == get_translation(message.chat.id, 'complaint_button'))
def complaint_box(message):
    bot.send_message(message.chat.id, get_translation(message.chat.id, 'enter_complaint'))
    bot.register_next_step_handler(message, save_complaint)

def save_complaint(message):
    with open('complaints.txt', 'a') as f:
        f.write(f"{message.chat.username}: {message.text}\n")
    bot.send_message(message.chat.id, get_translation(message.chat.id, 'complaint_recorded'))

bot.polling(none_stop=True)
