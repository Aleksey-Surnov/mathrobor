import asyncio
import asyncpg
import datetime

def command(func):
    async def wrapper(self, *args, **kwargs):
        cursor = await self._get_connection()#.cursor()                   # открываем курсор
        res = await func(self, *args, cursor=cursor, **kwargs)      # выполняем функцию
        self._get_connection().commit()                             # коммит, если он нужен
        cursor.close()                                              # закрываем курсор
        return res
    return wrapper


class DbHelper():
    def __init__(self, db_name: str, user: str, password: str):
        self.db_name = db_name
        self.user = user
        self.password = password
        self._connection = None

    async def _get_connection(self):
        if not self._connection:
            self._connection = await asyncpg.connect(host='localhost', database=self.db_name, user=self.user, password=self.password)
        return self._connection

    def __del__(self):
        if self._connection:
            self._connection.close()

    @command
    async def init_db(self, cursor, force: bool = False):
        if force:
            await cursor.execute('DROP TABLE IF EXISTS pay_info')
            await cursor.execute('DROP TABLE IF EXISTS user_info')

            self._connection.commit()


        await cursor.execute('''CREATE TABLE IF NOT EXISTS pay_info (
                                   id              SERIAL PRIMARY KEY,
                                   pay_true        BOOLEAN,
                                   datatime        DATE,
                                   user_id         INTEGER NOT NULL)''')

        await cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                                   id              SERIAL PRIMARY KEY,
                                   now_ball        INTEGER,
                                   past_ball       INTEGER,
                                   userID          SMALLINT REFERENCE pay_info(id))''')

    @command
    async def insert_db_pay_info(self, cursor, pay_true, date_time, user_id):
        await cursor.execute('INSERT INTO pay_info (pay_true, datatime, user_id) VALUES (%s, %s, %s)',
                       (pay_true, date_time, user_id))

    @command
    async def verify_user(self, cursor, user_id):
        await cursor.execute('SELECT user_id FROM pay_info WHERE user_id= %s', user_id)
        return cursor.fetchall()

    @command
    async def select_table(self, cursor):
        cursor.execute('SELECT * FROM user_info')
        return await cursor.fetchall()





