import os, json, time
import asyncio
from aiogram import Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Robotmath import mathrobot
from DBmodul import dbmodul

from config import TOKEN, admin_id, db_name, db_user, db_pass, host

loop = asyncio.get_event_loop()

vd = dbmodul.DbHelper(db_name, db_user, db_pass)
db = loop.run_until_complete(vd.init_db())
robot = mathrobot.Telegrammbot(TOKEN, vd, admin_id)
dp = Dispatcher(robot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    return await robot.start(message=message)


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)