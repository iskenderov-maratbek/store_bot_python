import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('database.db')
    cur = base.cursor()
    if base:
        print("Connected to database.......")
    base.execute("CREATE TABLE IF NOT EXISTS menu(img TEXT,name TEXT PRIMARY KEY, description TEXT,price TEXT)")
    base.commit()


# Управление продуктами в базе данных
async def sql_add(state):  # Добавление продукта в базу данных
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_delete(callback):  # Удаление продукта из базы данных
    cur.execute('DELETE FROM menu WHERE name=?', (callback.data,))
    base.commit()


async def sql_read(callback):  # Чтение всех продуктов из базы данных
    bot = callback.bot
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(callback.from_user.id, photo=ret[0],
                             caption=f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


async def sql_update(state):
    async with state.proxy() as data:
        cur.execute('UPDATE menu SET name=?,description=?,price=? WHERE img=?', tuple(data.values()))
        base.commit()

async def sql_add_category(name):
    cur.execute('INSERT INTO category VALUES(?)', (name,))
    base.commit()
