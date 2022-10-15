START_MSG = """<b>
Hey 👋,
Im group manager bot, to get start add me to your group and give admin permission.
</b>"""
HELP_MSG = """<b>
hey 👋، here some features of bot:

👤 Admin commands:
-----------------
'ban'
⛔️ Reply this command to message of user that you want to ban, you can unban him/her with glass button appeared further, also you can use 'pban' command to permanently ban any user.

'del'
❌ Reply on message to delete it

'+10'
⭐️ give 10 score to targeted user, by replying on their message.
-----------------


👥 User commands:
-----------------
'+'
⭐️ Use to give 1 score to user by replying to their messages.
'stat'
📲 Get stats about your profile

-----------------


Made with 🤍 by <a href='tg://user?username=MurphySpiderDev'>[MurphySpider]</a>
</b>"""

RULES_MSG = """<b>🔻 Group rules

🔵 No rude discussion

🔵 Dont spam with links 

🔵 No politician discussion 

🔵 Use /help command to get bot features list


Made with 🤍 by <a href='tg://user?username=MurphySpiderDev'>[MurphySpider]</a></b>"""

# here is list of rude words, add your list in this list, bot will read and check rude words in messages from these lists

# for combo words
RUDE = [
    "mother f**ker",
    "sh*t face",
]
# for single words
RUDE_SINGLE = [
    "f*cker",
    "sh*t",
]

NO_RUDE = """<b>
Your message deleted, please respect each other and dont use rude words.
</b>"""
