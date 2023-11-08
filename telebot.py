import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler
import json
import time
import asyncio
import random


from namepar import GainNamePar
from secrets import TOKEN

massnamepar = GainNamePar()
print(massnamepar)
count = 1
keyboard = []
message = ""
for name in massnamepar:
    message += "(" + str(count) + ") " + str(name[1]) + " - " + str(name[3]) + "\n"
    keyboard.append([
        InlineKeyboardButton("(" + str(count) + ")" + " ПР", callback_data=count),
        InlineKeyboardButton("(" + str(count) + ")" + " От/УвП", callback_data=count+1),
        InlineKeyboardButton("(" + str(count) + ")" + " Др/П", callback_data=count+2)
    ])
    count+=3
keyboard.append([
        InlineKeyboardButton("Отмена", callback_data=99),
        InlineKeyboardButton("Отметить", callback_data=98),
    ])
print(keyboard)
message += "\n" + "Кто присутсвовал?"
callback_value = []
students = {}
temporarily_names = []
queue = asyncio.Queue()
arr_fio_users = []
tasks = []
query_text_last = ""
type_button = " - Др/ПГ"

with open("table.json", encoding='utf-8') as f:
    ID_TABLE = json.load(f)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello, {update.effective_user.first_name}')

async def sex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Ты заставлял меня сосать, но я тебе не сосала \n Заставлял меня сосать, но я тебе отказала \n Попросил тебя сосать, ты же мне пообещала \n Попросил тебя сосать, а в итоге наебал \n Ты заставлял меня сосать, но я тебе не сосала \n Заставлял меня сосать, но я тебе отказала \nПопросил тебя сосать, ты же мне пообещала \nПопросил тебя сосать, а в итоге наебала \nЯ-Я-Я-Я растворилась в тебе, но я не сахар в воде \nДелаешь больно ты мне, но у меня иммунитет \nИ что теперь? Что теперь? Закрой свой рот, закрой дверь \nНе буду делать минет, лучше соси сам себе \nКаждый день ты хочешь секс, будто ты голодный \nТебе нехуй больше делать, ты же безработный \nЧерез три минуты секса ты весь уже потный \nЯ ушла от тебя, теперь ты свободный \nТы заставлял меня сосать, но я тебе не сосала \nЗаставлял меня сосать, но я тебе отказала \nПопросил тебя сосать, ты же мне пообещала \nПопросил тебя сосать, а в итоге наебала-бала-бала \nО-Она любит делать грязь, я наладил с нею связь \nНе хочу ничё скрывать, я хочу тебя еб (А-а-а) \nОна не любит делать это, она любит (Ах) \nЯ предложил ей пососать, но у неё есть друг \nМы оба знаем, это было лишь в моих мечтах \nНо ты была со мною будто бы в последний раз \nДа, я набираю её, она сама не звонит \nОткрывает свой рот, только когда говорит \nИ её голос меня так притянул как магнит \nЯ знаю, что у меня на неё есть безлимит \nЗаставлял меня сосать, ты меня сосать, а-а-а-а \nМеня сосать, ты меня сосать, а-а-а-а-а-а-а-а-а \nСосать, ты меня сосать, а-а-а-а \nМеня сосать, ты меня сосать \nТы заставлял меня сосать, но я тебе не сосала \nЗаставлял меня сосать, но я тебе отказала \nПопросил тебя сосать, ты же мне пообещала \nПопросил тебя сосать, а в итоге наебала \nЗаставлял меня сосать')
async def anek(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("anek.json", "r", encoding="utf-8") as f:
        p = json.load(f)
        num = random.randrange(len(p))
        await update.message.reply_text(f'{p[num]}')


async def perekl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    print(ID_TABLE["admin"], user_id)
    if(str(user_id) == str(ID_TABLE["admin"])):

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        await update.message.reply_text(f'У тебя нет прав на это действие')



async def buttons(update, context):
    global type_button
    query = update.callback_query
    user_id = str(query.from_user.id)
    reply_markup = InlineKeyboardMarkup(keyboard)
    if user_id in ID_TABLE:
        name = ID_TABLE[user_id]
        if int(query.data) != 98 and int(query.data) != 99:
            NumberOfButtons = len(massnamepar) * 3
            PressedButton = int(query.data)
            RowCounter = 1
            print(name+ str(RowCounter))
            print(arr_fio_users)
            if name+ str(RowCounter) in arr_fio_users:
                arr_fio_users.remove(name+ str(RowCounter))
            for i in range(1, NumberOfButtons):
                if i == PressedButton:
                    if PressedButton == RowCounter:
                        type_button = " - Пр"
                        arr_fio_users.append(name + str(RowCounter))
                        break
                    elif PressedButton == RowCounter+1:
                        type_button = " - От/УвП"
                        arr_fio_users.append(name + str(RowCounter))
                        break
                    else:
                        arr_fio_users.append(name + str(RowCounter))


                    if i %3 == 0 and i not in (1, 2, 3):
                        RowCounter+=1
                temporarily_names.append(name + " (" + str(RowCounter) + ")" + type_button)
                type_button = " - Др/ПГ"
                name_user = json.dumps(temporarily_names, indent=4)
                with open("bd_add_user.json", "w", encoding="utf-8") as f:
                    f.write(name_user)
    #                name_sorting = sorted([name] + query_text[2:])
    #                people = str(len(name_sorting))
    #                query_text = "\n".join([f"{message} ({people})\n"] + name_sorting)
    #                await query.edit_message_text(text=f"{query_text}", reply_markup=reply_markup)

    await query.answer()
    with open("bd_add_user.json", "r+", encoding="utf-8") as f:
        temporarily_names_arr = json.load(f)
        len_arr_names = len(temporarily_names_arr)
        query_text = "\n".join([f"{message} ({len_arr_names})\n"] + temporarily_names_arr)
        if query_text != query.message.text:
            await query.edit_message_text(text=f"{query_text}", reply_markup=reply_markup)










    name = ID_TABLE[user_id]
    if int(query.data) == 1:
        if name + "1" in callback_value:
            callback_value.remove(name + "1")
        if name + "4" in callback_value:
            callback_value.remove(name + "4")
        if name + "5" in callback_value:
            callback_value.remove(name + "5")
        if name in arr_fio_users:
            arr_fio_users.remove(name)
        callback_value.append(name + "1")
        arr_fio_users.append(name)
    elif int(query.data) == 4:
        if name + "1" in callback_value:
            callback_value.remove(name + "1")
        if name + "4" in callback_value:
            callback_value.remove(name + "4")
        if name + "5" in callback_value:
            callback_value.remove(name + "5")
        if name in arr_fio_users:
            arr_fio_users.remove(name)
        callback_value.append(name + "4")
        arr_fio_users.append(name)
    elif int(query.data) == 5:
        if name + "1" in callback_value:
            callback_value.remove(name + "1")
        if name + "4" in callback_value:
            callback_value.remove(name + "4")
        if name + "5" in callback_value:
            callback_value.remove(name + "5")
        if name in arr_fio_users:
            arr_fio_users.remove(name)
        callback_value.append(name + "5")
        arr_fio_users.append(name)

    elif int(query.data) == 99 and name in query_text:
        with open("bd_add_user.json", "w", encoding="utf-8") as f:
            temporarily_names.remove(name)
            json.dump(temporarily_names, f)
        arr_fio_users.remove(name)
        if name + "1" in callback_value:
            callback_value.remove(name + "1")
        if name + "4" in callback_value:
            callback_value.remove(name + "4")
        if name + "5" in callback_value:
            callback_value.remove(name + "5")
        with open("bd_add_user.json", "r+", encoding="utf-8") as f:
            temporarily_names_arr = json.load(f)
            print(temporarily_names_arr)
            len_arr_names = len(temporarily_names_arr)
            query_text = "\n".join([f"{message} ({len_arr_names})\n"] + temporarily_names_arr)
            await query.edit_message_text(text=f"{query_text}", reply_markup=reply_markup)

    elif int(query.data) == 98:
        if user_id == ID_TABLE["admin"]:
            await query.edit_message_text(text=f"{query_text}", reply_markup='')
            with open("present_names.json", "w", encoding="utf-8") as f:
                print(arr_fio_users,callback_value)
                for count_value in range(len_arr_names):
                    students[arr_fio_users[count_value]] = int(callback_value[count_value][-1])
                json.dump(students, f, ensure_ascii=False, indent=4)
            from parser import checkPresent
            checkPresent()
            query_text = query.message.text
            await query.edit_message_text(text=f"{query_text}\nОтметил🎉", reply_markup='')

    #        else:
    #            print(query.from_user)
    # time.sleep(0.5)


async def worker():
    while True:
        sleep_for = await queue.get()
        await asyncio.sleep(sleep_for)

        queue.task_done()


async def update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        print(context)
        await queue.join()
        queue.put_nowait(buttons(update, context))
        task = asyncio.create_task(worker())
        tasks.append(task)
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

        asyncio.wait_for(buttons(update, context))


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("hello", hello))

    app.add_handler(CommandHandler("sex", sex))

    app.add_handler(CommandHandler("perekl", perekl))

    app.add_handler(CommandHandler("anek", anek))

    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()
