import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import admin
import client
from database import initialize_db
from config import TOKEN

# Логирование для отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Инициализация базы данных
initialize_db()

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Администратор", callback_data='admin')],
        [InlineKeyboardButton("Клиент", callback_data='client')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать в салон красоты!\nВыберите роль:", reply_markup=reply_markup)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Добавить мастера", callback_data='add_master')],
        [InlineKeyboardButton("Добавить услугу", callback_data='add_service')],
        [InlineKeyboardButton("Показать всех мастеров", callback_data='view_masters')],
        [InlineKeyboardButton("Показать все услуги", callback_data='view_services')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Панель администратора:", reply_markup=reply_markup)

async def client_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Записаться на услугу", callback_data='book_appointment')],
        [InlineKeyboardButton("Показать все записи", callback_data='view_appointments')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Панель клиента:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'admin':
        await admin_panel(update, context)
    elif query.data == 'client':
        await client_panel(update, context)
    elif query.data == 'add_master':
        await query.message.reply_text("Введите имя мастера и его специализацию через запятую:")
        context.user_data['action'] = 'add_master'
    elif query.data == 'add_service':
        await query.message.reply_text("Введите название услуги, длительность (мин), цену и ID мастера через запятую:")
        context.user_data['action'] = 'add_service'
    elif query.data == 'view_masters':
        masters = admin.view_masters()
        response = "\n".join([f"{master[0]}. {master[1]} - {master[2]}" for master in masters])
        await query.message.reply_text(f"Мастера:\n{response}")
    elif query.data == 'view_services':
        services = admin.view_services()
        response = "\n".join([f"{service[0]}. {service[1]} - {service[2]} мин, {service[3]} руб." for service in services])
        await query.message.reply_text(f"Услуги:\n{response}")
    elif query.data == 'book_appointment':
        await query.message.reply_text("Введите ваше имя, ID услуги и дату (YYYY-MM-DD HH:MM) через запятую:")
        context.user_data['action'] = 'book_appointment'
    elif query.data == 'view_appointments':
        appointments = client.view_appointments()
        response = "\n".join([f"{appt[1]} записан на {appt[2]} к {appt[4]} ({appt[3]})" for appt in appointments])
        await query.message.reply_text(f"Записи:\n{response}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get('action')

    if action == 'add_master':
        name, specialty = update.message.text.split(',')
        admin.add_master(name.strip(), specialty.strip())
        await update.message.reply_text(f"Мастер {name.strip()} добавлен.")
    elif action == 'add_service':
        name, duration, price, master_id = update.message.text.split(',')
        admin.add_service(name.strip(), int(duration.strip()), float(price.strip()), int(master_id.strip()))
        await update.message.reply_text(f"Услуга {name.strip()} добавлена.")
    elif action == 'book_appointment':
        client_name, service_id, appointment_date = update.message.text.split(',')
        client.book_appointment(client_name.strip(), int(service_id.strip()), appointment_date.strip())
        await update.message.reply_text(f"Запись для {client_name.strip()} добавлена.")
    
    context.user_data['action'] = None

# Основная функция для запуска бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
