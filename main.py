import time
from telegram import *
from telegram.ext import *
import consts
import db
import messages


TOKEN = "<YOUR BOT TOKEN HERE>"

WM = None

def start(update: Update, context: CallbackContext):
    update.message.reply_text(text=messages.START_MSG, parse_mode=ParseMode.HTML)


def help(update: Update, context: CallbackContext):
    update.message.reply_text(text=messages.HELP_MSG, parse_mode=ParseMode.HTML)


def echo(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_msg = update.message.text
    message = update.message

    uid = update.effective_user.id
    fname = update.effective_user.full_name
    username = update.effective_user.username
    check = db.check_user(uid)
    if check == 0:
        db.add_user(uid=uid, name=fname, username=username, admin='0', score='0')
        context.bot.send_message(chat_id=consts.MAIN_ADMIN, text=f"username:{username},name:{fname} added to database")

    for i in range(len(messages.RUDE)):
        if messages.RUDE[i] in user_msg:
            bmsg = update.message.reply_text(text=messages.NO_RUDE, parse_mode=ParseMode.HTML)
            message.delete()
            # btimer = 60
            # while True:
            #     btimer = btimer - 1
            #     time.sleep(1)
            #     if btimer == 0:
            #         bmsg.delete()
            #         break

    for i in range(len(messages.RUDE_SINGLE)):
        if messages.RUDE_SINGLE[i] == user_msg:
            bmsg = update.message.reply_text(text=messages.NO_RUDE, parse_mode=ParseMode.HTML)
            message.delete()
            # btimer = 60
            # while True:
            #     btimer = btimer - 1
            #     time.sleep(1)
            #     if btimer == 0:
            #         bmsg.delete()
            #         break

    if user_msg == "test" or user_msg == "Test":
        update.message.reply_text(text="<b>For testing bot use private chat!</b>",
                                  parse_mode=ParseMode.HTML)


    if user_msg == "users" and user_id == consts.MAIN_ADMIN:
        users = db.get_users()
        update.message.reply_text(text=f"Confirmed users count: {users}")

    if user_msg == "fix" and user_id == consts.MAIN_ADMIN:
        db.fix_users()
        update.message.reply_text(text="<b>Users list fixed.</b>", parse_mode=ParseMode.HTML)

    if user_msg == "ban" or user_msg == "Ban":
        if db.is_admin(user_id) == 1:
            uid = update.message.reply_to_message.from_user.id
            uname = update.message.reply_to_message.from_user.full_name
            db.del_user(uid)
            keyboard = [
                [InlineKeyboardButton("Unban ☑️", callback_data=str(uid) + " unban")]
            ]
            mention = f"<a href='tg://user?id={uid}'>{uname}</a> "
            update.message.reply_text(f"User [ {mention} ] banned by admin.", parse_mode=ParseMode.HTML,
                                      reply_markup=InlineKeyboardMarkup(keyboard))
            context.bot.ban_chat_member(user_id=uid, chat_id=chat_id)
            context.bot.unban_chat_member(user_id=uid, chat_id=chat_id)
            message.delete()
            print(f"user {uid} banned and unbanned!")
        else:
            update.message.reply_text(text="<b>You dont have permission!</b>", parse_mode=ParseMode.HTML)

    if user_msg == "del" or user_msg == "Del":
        if db.is_admin(user_id) == 1:
            mid = update.message.reply_to_message.message_id
            context.bot.delete_message(message_id=mid, chat_id=chat_id)
            message.delete()
        else:
            update.message.reply_text(text="<b>You dont have permission!</b>", parse_mode=ParseMode.HTML)

    if "gay" in user_msg or "Gay" in user_msg:
        update.message.reply_text("<b>Please stop rude discussion.</b>", parse_mode=ParseMode.HTML)
        message.delete()

    if user_msg == "stat" or user_msg == "Stat":
        uname = update.effective_user.username
        name = update.effective_user.full_name
        uid = update.effective_user.id
        uscore = db.get_score(uid)
        ugift = db.get_gift(uid)
        info = f"""---
📲 Username: <code>{uname}</code>

👤 Fullname: <b>{name}</b>

🔹 UID: <code>{uid}</code>

🌟 Your score: <b>{uscore}</b>

⭐️ Available scores to give: <b>{ugift}</b>

---"""
        update.message.reply_text(text=info, parse_mode=ParseMode.HTML)

    if user_msg == "pban":
        if db.is_admin(user_id) == 1:
            uid = update.message.reply_to_message.from_user.id
            uname = update.message.reply_to_message.from_user.full_name
            keyboard = [
                [InlineKeyboardButton("Unban ☑️", callback_data=str(uid) + " unban")]
            ]
            mention = f"<a href='tg://user?id={uid}'>{uname}</a> "
            update.message.reply_text(f"User [ {mention} ] permanently banned by admin.",
                                      parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

            context.bot.ban_chat_member(user_id=uid, chat_id=chat_id)
            print(f"user {uid} permanently banned!")
        else:
            update.message.reply_text(text="<b>You dont have permission!</b>", parse_mode=ParseMode.HTML)
    if user_msg == "+":
        uid = update.message.reply_to_message.from_user.id
        uname = update.message.reply_to_message.from_user.full_name
        if uid != user_id:
            db.add_score(score="1", uid=uid)
            update.message.reply_text(text="<b>🌟 User received 1 score from you!</b>",
                                      parse_mode=ParseMode.HTML)
            # message.delete()
        else:
            update.message.reply_text(text="<b>Nope you cant give score to yourself 😏</b>", parse_mode=ParseMode.HTML)

    if user_msg == "+10" and db.is_admin(user_id):
        uid = update.message.reply_to_message.from_user.id
        if uid != user_id:
            db.add_score(score="10", uid=uid)
            update.message.reply_text(text="<b>🌟 User received 10 score from you!</b>",
                                      parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(text="<b>Nope you cant give score to yourself 😏</b>", parse_mode=ParseMode.HTML)

    if user_msg == "add" and user_id == consts.MAIN_ADMIN:
        uid = update.message.reply_to_message.from_user.id
        db.add_admin(uid=uid)
        msg = "<b>User added to admin list, use /help command to see how to use admin commands.</b>"
        update.message.reply_text(text=msg, parse_mode=ParseMode.HTML)


def on_ban(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)


def button(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    q = update.callback_query
    q.answer()
    if "unban" not in q.data:
        cdata = q.message.reply_markup.inline_keyboard[0][0].callback_data
        uid = q.from_user.id
        print(q)
        print("call back", cdata)
        print("id", q.message.entities[0].user.id)
        if str(cdata) == str(uid):
            mention = f"<a href='tg://user?id={uid}'>Your</a> "
            msg = f"restriction {mention} has been removed 🟢️"
            m = context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML)
            context.bot.restrict_chat_member(chat_id=chat_id, user_id=uid, permissions=
            ChatPermissions(can_send_messages=True,
                            can_invite_users=True,
                            can_send_other_messages=True,
                            can_send_media_messages=True))

            q.edit_message_reply_markup(reply_markup=None)
            while True:
                time.sleep(3)
                m.delete()
                break
        else:
            mention = f"<a href='tg://user?id={uid}'>Dont</a> "
            fool = f"{mention} touch!"
            m = context.bot.send_message(chat_id=chat_id, text=fool, parse_mode=ParseMode.HTML)
            while True:
                time.sleep(2)
                m.delete()
                break
    else:
        uid = q.data.split(" ")
        context.bot.unban_chat_member(chat_id=chat_id, user_id=uid[0])
        q.edit_message_reply_markup(reply_markup=None)
        context.bot.send_message(chat_id=chat_id, text="<b>User removed from ban list.</b>",
                                 parse_mode=ParseMode.HTML)


def on_join(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    new_users_count = len(update.message.new_chat_members)
    chat_title = update.effective_chat.title
    for i in range(new_users_count):
        uid = update.message.new_chat_members[i].id
        uname = update.message.new_chat_members[i].full_name
        username = update.message.new_chat_members[i].username
        db.add_user(uid=uid, score="0", name=uname, username=username, admin="0")
        context.bot.restrict_chat_member(chat_id=chat_id, user_id=uid,
                                         permissions=ChatPermissions(can_send_messages=False))
        mention = f"<a href='tg://user?id={uid}'>{uname}</a> "
        welcom = f"""Hey 👋 [{mention}] dear {chat_title} welcom!
please click on im not bot to make sure your a real person!"""
        keyboard = [
            [InlineKeyboardButton(text="Im not bot!✅", callback_data=str(uid))]
        ]
        reply_keyabord = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text=welcom, parse_mode=ParseMode.HTML, reply_markup=reply_keyabord)
        print(update.message.new_chat_members[i])


def on_status(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)


def rules(update: Update, context: CallbackContext):
    update.message.reply_text(text=messages.RULES_MSG, parse_mode=ParseMode.HTML)


def fix_users(context:CallbackContext):
    db.fix_users()
    print("fix users performed!")


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    jobq = JobQueue()
    jobq.set_dispatcher(dispatcher=dispatcher)
    jobq.run_repeating(callback=fix_users, interval=1)
    dispatcher.add_handler(CommandHandler("start", start, run_async=True))
    dispatcher.add_handler(CommandHandler("help", help, run_async=True))
    dispatcher.add_handler(CommandHandler("rules", rules, run_async=True))
    dispatcher.add_handler(MessageHandler(filters=Filters.text & ~Filters.command, callback=echo, run_async=True))
    dispatcher.add_handler(
        MessageHandler(filters=Filters.status_update.left_chat_member, callback=on_ban, run_async=True))
    dispatcher.add_handler(
        MessageHandler(filters=Filters.status_update.left_chat_member, callback=on_status, run_async=True))
    dispatcher.add_handler(
        MessageHandler(filters=Filters.status_update.new_chat_members, callback=on_join, run_async=True))
    dispatcher.add_handler(
        MessageHandler(filters=Filters.status_update.new_chat_title, callback=on_status, run_async=True))
    dispatcher.add_handler(
        MessageHandler(filters=Filters.status_update.new_chat_title, callback=on_status, run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(button, run_async=True))
    print("bot is running....")
    updater.start_polling()
    # jobq.start()
    updater.idle()


if __name__ == "__main__":
    main()
