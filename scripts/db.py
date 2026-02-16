import sqlite3

def create_chat_log():
    print('creating chat.db file with chat_log table')
    con = sqlite3.connect("configs/chat.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS chat_log")
    cur.execute("CREATE TABLE chat_log(user, time, msg)")
    con.commit()
    con.close()
