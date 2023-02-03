import asyncio
from pathlib import Path

import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton

from converbot.bot_utils import parse_context, create_conversation_from_context
from converbot.constants import DEFAULT_CONFIG_PATH
from converbot.database import ConversationDB

CONVERSATIONS_DB = ConversationDB()

API_TOKEN = (Path(__file__).parent / "token.txt").read_text().strip().replace("\n", "")

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

RESTART_KEYBOARD = types.ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton('/start')]], resize_keyboard=True, one_time_keyboard=True
)


@dispatcher.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_chat_action(message.from_user.id, action=types.ChatActions.TYPING)
    await asyncio.sleep(1)

    await bot.send_message(message.from_user.id, text="Hello! Welcome to Your Best Companion Bot!")
    await asyncio.sleep(1)

    await bot.send_message(
        message.from_user.id,
        text="Please, provide initial context. Format: Name, Age, Interests, Profession, Gender"
    )
    await asyncio.sleep(1)

    await bot.send_message(
        message.from_user.id,
        text="Example: Alisa, 25, Guitar, Python Programmer, Female",
        reply_markup=RESTART_KEYBOARD
    )
    await asyncio.sleep(0.5)

    CONVERSATIONS_DB.remove_conversation(message.from_user.id)


@dispatcher.message_handler()
async def handle_message(message: types.Message) -> None:

    if message.text.startswith("/"):
        conversation = CONVERSATIONS_DB.get_conversation(message.from_user.id)
        conversation.set_tone(message.text[1:])
        return None

    # Try to handle context
    if CONVERSATIONS_DB.exists(message.from_user.id) is False:
        context = parse_context(message.text)
        if context is None:
            await bot.send_message(message.from_user.id, text="Wrong context format. Try again.")
            await asyncio.sleep(1)

            await bot.send_message(
                message.from_user.id,
                text="Please, provide initial context. Format: Name, Age, Interests, Profession, Gender"
            )
            await asyncio.sleep(1)

        conversation = create_conversation_from_context(context, config_path=DEFAULT_CONFIG_PATH)
        CONVERSATIONS_DB.add_conversation(message.from_user.id, conversation)
        CONVERSATIONS_DB.write_chat_history(message.from_user.id, message.text, chatbot_response="None")

        await bot.send_message(message.from_user.id, text="Let's start the conversation!")
        return None

    # Handle conversation
    await bot.send_chat_action(message.from_user.id, action=types.ChatActions.TYPING)
    await asyncio.sleep(2)

    conversation = CONVERSATIONS_DB.get_conversation(message.from_user.id)
    chatbot_response = conversation.ask(message.text)

    CONVERSATIONS_DB.write_chat_history(message.from_user.id, message.text, chatbot_response)

    await bot.send_message(message.from_user.id, text=chatbot_response)


async def serialize_conversation_task():
    # CONVERSATIONS_DB.serialize_conversations()
    pass


async def scheduler():
    aioschedule.every(60).seconds.do(serialize_conversation_task)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False, on_startup=on_startup)
