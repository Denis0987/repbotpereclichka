import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler
import json
import time

from secrets import TOKEN
from parser import checkPresent

message = "Кто присутсвовал?"
callback_value = []
students = {}
arr_fio_users = []
with open("table.json", encoding='utf-8') as f:
    ID_TABLE = json.load(f)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello, {update.effective_user.first_name}')


async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Присутствовал", callback_data=1)],
        [InlineKeyboardButton("Отмена", callback_data=2)],
        [InlineKeyboardButton("Отсутствовал по ув.п.", callback_data=4)],
        [InlineKeyboardButton("Отметить", callback_data=3)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup)


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Присутствовал", callback_data=1)],
        [InlineKeyboardButton("Отмена", callback_data=2)],
        [InlineKeyboardButton("Отсутствовал по ув.п.", callback_data=4)],
        [InlineKeyboardButton("Отметить", callback_data=3)]
    ]
    query = update.callback_query
    user_id = str(query.from_user.id)
    reply_markup = InlineKeyboardMarkup(keyboard)
    query_text = query.message.text.split("\n")
    if user_id in ID_TABLE:
        name = ID_TABLE[user_id]
        if int(query.data) != 3 and int(query.data) != 2:
            if not (name in arr_fio_users):
                name_sorting = sorted([name] + query_text[2:])
                people = str(len(name_sorting))
                print(name_sorting)
                query_text = "\n".join([f"{message} ({people})\n"] + name_sorting)
                await query.edit_message_text(text=f"{query_text}", reply_markup=reply_markup)
    else:
        name = query.from_user.first_name + " " + user_id

    await query.answer()

    if int(query.data) == 1:
        if name + "1" in callback_value:
            callback_value.remove(name + "1")
            arr_fio_users.remove(name)
        if name + "4" in callback_value:
            callback_value.remove(name + "4")
            arr_fio_users.remove(name)
        callback_value.append(name + "1")
        arr_fio_users.append(name)

    elif int(query.data) == 4:
        if name + "1" in callback_value:
            callback_value.remove(name + "1")
            arr_fio_users.remove(name)
        if name + "4" in callback_value:
            callback_value.remove(name + "4")
            arr_fio_users.remove(name)
        callback_value.append(name + "4")
        arr_fio_users.append(name)

    elif int(query.data) == 2 and name in query_text:
        query_text.remove(name)
        arr_fio_users.remove(name)
        if name + "1" in callback_value:
            callback_value.remove(name + "1")
        if name + "4" in callback_value:
            callback_value.remove(name + "4")
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
                    students[arr_fio_users[count_value]] = int(callback_value[count_value][-1])
                json.dump(students, f, ensure_ascii=False, indent=4)

            checkPresent()

            await query.edit_message_text(text=f"{query_text}\nОтметил🎉", reply_markup=reply_markup)

        else:
            print(query.from_user)
    # time.sleep(0.5)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("hello", hello))

    app.add_handler(CommandHandler("perecklichka", poll))

    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()
