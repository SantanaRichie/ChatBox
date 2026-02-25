import sqlite3

def create_chat_log():
    print('creating chat.db file with chat_log table')
    con = sqlite3.connect("configs/chat.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS chat_log")
    cur.execute("CREATE TABLE chat_log(user, time, msg)")
    con.commit()
    con.close()

def create_connections_db():
    print('creating connections.db file with connections table')
    con = sqlite3.connect("configs/connections.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS connections")
    cur.execute("""CREATE TABLE connections(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user1 TEXT NOT NULL,
        user2 TEXT NOT NULL,
        user2_host TEXT,
        user2_port INTEGER DEFAULT 5000,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    con.commit()
    con.close()

create_chat_log()
create_connections_db()
