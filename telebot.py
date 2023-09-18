from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler
import json

from secrets import TOKEN
from parser import checkPresent

message = "Кто присутствовал?"
callback_value = []
students = {}
with open("table.json", encoding='utf-8') as f:
    ID_TABLE = json.load(f)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello, {update.effective_user.first_name}')


async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
            [InlineKeyboardButton("Присутствовал", callback_data=1)],
            [InlineKeyboardButton("Отсутствовал", callback_data=2)],
            [InlineKeyboardButton("Отсутствовал по ув.п.", callback_data=4)],
            [InlineKeyboardButton("Отметить", callback_data=3)]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup)


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    user_id = str(query.from_user.id)

    if user_id in ID_TABLE:
        name = ID_TABLE[user_id]
    else:
        name = query.from_user.first_name + " " + user_id

    query_text = query.message.text.split("\n")

    await query.answer()

    keyboard = [
            [InlineKeyboardButton("Присутствовал", callback_data=1)],
            [InlineKeyboardButton("Отсутствовал", callback_data=2)],
            [InlineKeyboardButton("Отсутствовал по ув.п.", callback_data=4)],
            [InlineKeyboardButton("Отметить", callback_data=3)]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if int(query.data) == 1 and name not in query_text:
        callback_value.append(1)
        name_sorting = sorted([name] + query_text[2:])
        people = str(len(name_sorting))

        query_text = "\n".join([f"{message} ({people})\n"] + name_sorting)
        await query.edit_message_text(text=f"{query_text}", reply_markup=reply_markup)

    elif int(query.data) == 4 and name not in query_text:
        callback_value.append(4)
        name_sorting = sorted([name] + query_text[2:])
        people = str(len(name_sorting))

        query_text = "\n".join([f"{message} ({people})\n"] + name_sorting)
        await query.edit_message_text(text=f"{query_text}", reply_markup=reply_markup)

    elif int(query.data) == 2 and name in query_text:
        query_text.remove(name)

        name_sorting = sorted(query_text[2:])
        people = str(len(name_sorting))

        query_text = "\n".join([f"{message} ({people})\n"] + name_sorting)
        await query.edit_message_text(text=f"{query_text}", reply_markup=reply_markup)

    elif int(query.data) == 3:
        if user_id == ID_TABLE["admin"]:
            names = query_text[2:]
            query_text = "\n".join(query_text)
            await query.edit_message_text(text=f"{query_text}")

            with open("present_names.json", "w", encoding="utf-8") as f:
                for count_value in range(len(names)):
                    students[names[count_value]] = callback_value[count_value]
                json.dump(students, f, ensure_ascii=False, indent=4)

            checkPresent()

            await query.edit_message_text(text=f"{query_text}\nSucess! 🎉",reply_markup=reply_markup)

        else:
            print(query.from_user)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("hello", hello))

    app.add_handler(CommandHandler("poll", poll))

    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()
