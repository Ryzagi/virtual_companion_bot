import asyncio
import os
import json

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
    keyboard=[[KeyboardButton('/start')], [KeyboardButton('/debug')]], resize_keyboard=True,
    one_time_keyboard=True
)

IS_DEBUG = False


@dispatcher.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_chat_action(message.from_user.id, action=types.ChatActions.TYPING)

    await bot.send_message(
        message.from_user.id,
        text="Hello! Welcome to Your Best Companion Bot!\n\n"
        "Please, provide initial context. Format: Name, Age, Interests, Profession, Gender\n\n"
        "Example: Alisa, 25, Guitar, Python Programmer, Female",
        reply_markup=RESTART_KEYBOARD
    )
    await asyncio.sleep(1)

    CONVERSATIONS_DB.remove_conversation(message.from_user.id)


@dispatcher.message_handler(commands=["debug"])
async def debug(message: types.Message):
    conversation = CONVERSATIONS_DB.get_conversation(message.from_user.id)
    if conversation is None:
        await bot.send_message(message.from_user.id,
                         text="Please, provide initial context. Format: Name, Age, Interests, Profession, Gender")
    state = conversation.change_debug_mode()
    if state:
        await bot.send_message(message.from_user.id, text="«Debug mode on»\nPlease continue the discussion with your companion")
    else:
        await bot.send_message(message.from_user.id, text="«Debug mode off»\nPlease continue the discussion with your companion")

    #config = read_json_file(DEFAULT_CONFIG_PATH)
    #await bot.send_message(message.from_user.id, text=config["prompt_template"])


@dispatcher.message_handler()
async def handle_message(message: types.Message) -> None:

    if message.text.startswith("/"):
        conversation = CONVERSATIONS_DB.get_conversation(message.from_user.id)
        conversation.set_tone(message.text[1:])

        await bot.send_chat_action(message.from_user.id, action=types.ChatActions.TYPING)
        await asyncio.sleep(1)

        await bot.send_message(message.from_user.id, text=f"Information «{message.text[1:]}» has been added.")
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

        # TODO: Move to separate function
        await bot.send_chat_action(message.from_user.id, action=types.ChatActions.TYPING)
        await asyncio.sleep(1.5)

        await bot.send_message(
            message.from_user.id,
            text="You are talking to:\n"
                f"Name: {context.name}\n"
                f"Age: {context.age}\n"
                f"Interests: {context.interests}\n"
                f"Profession: {context.profession}\n"
                f"Gender: {context.gender}\n"
        )
        await bot.send_chat_action(message.from_user.id, action=types.ChatActions.TYPING)
        await asyncio.sleep(1)

        await bot.send_message(message.from_user.id, text="Please initiate the discussion with your companion")
        return None

    # Handle conversation
    await bot.send_chat_action(message.from_user.id, action=types.ChatActions.TYPING)

    conversation = CONVERSATIONS_DB.get_conversation(message.from_user.id)
    chatbot_response = conversation.ask(message.text)
    CONVERSATIONS_DB.write_chat_history(message.from_user.id, message.text, chatbot_response)

    #await asyncio.sleep(len(chatbot_response) * 0.03)

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


def read_json_file(file_path):
    # Open the file
    with open(file_path, 'r') as file:
        # Load the JSON data
        data = json.load(file)
        # return the data
        return data

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False, on_startup=on_startup)
