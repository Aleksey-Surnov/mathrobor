import os, json
#from telebot import types
#import telebot
#from datetime import datetime, timedelta


import asyncio
import logging

from datetime import date, datetime, timedelta
from aiogram import Bot, md, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import Throttled

from DBmodul import dbmodul


class Telegrammbot(Bot):

    def __init__(self, TOKENBOT, databese, MANAGERID):
        Bot.__init__(self, token=TOKENBOT)
        self.bot = Bot(token=TOKENBOT)                                        # токен бота telegram.
        self.vd = databese                                                    # название базы данных
        self.managerid = int(MANAGERID)

    async def start(self, message):
        await self.bot.send_message(message.from_user.id, 'Hello. I am a robot that helps develop mathematical thinking. '
                                                          '\nI have two ways to train:'
                                                          '\n1. Arithmetic.'
                                                          '\n2. Logic.'
                                                          '\nIf you are ready to devote time to training for 15 minutes 2 times a day, then in 3 months you will see the result.'
                                                          '\nTo support the project, we ask you to pay for a training subscription.'
                                                          '\nPrice: 1 usd = 1 week.', parse_mode="Markdown")
        await self.bot.send_message(message.chat.id, "Make a selection by clicking the button:", reply_markup = await self.main_keybard())
        wer = await self.vd.verify_user(user_id=message.from_user.id)
        print(wer)
        if not bool(self.vd.verify_user(user_id=message.from_user.id)):                                          # на тот случай если пользователь несколько раз введет "/start".
            await self.vd.add_status(pay_true=False, datetime=datetime.today().date(), user_id=message.from_user.id)



    async def main_keybard(self):  # создаем клавиатуру выбора режимов.
        keyboardmain = types.InlineKeyboardMarkup()
        aritmetic_button = types.InlineKeyboardButton(text="Arithmetic", callback_data="arithmetic")
        logic_button = types.InlineKeyboardButton(text="Logic", callback_data="logic")
        keyboardmain.add(aritmetic_button)
        keyboardmain.add(logic_button)
        return keyboardmain


    async def init_db(self):
        return await self.vd.init_db()

