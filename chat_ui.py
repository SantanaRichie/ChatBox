import PySimpleGUI as sg
from datetime import datetime as dt
import sqlite3
import time
import threading
from chatNet_utils import get_drive_access, update_file

path = 'chat.db path'
creds, service = get_drive_access()

def the_thread(window):
    """
    The thread that communicates with the application through the window's events.

    Once a second wakes and sends a new event and associated value to the window
    """
    i = 0
    while True:
        time.sleep(5)
        window.write_event_value('-THREAD-', (threading.current_thread().name, i))      # Data sent is a tuple of thread name and counter
        i += 1

def refresh_chat():
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('Select time, user, msg from chat_log order by time asc')
    res = cur.fetchall()
    log = ''.join([f'{entry[0]}: {entry[1]}- {entry[2]}\n' for entry in res])
    return log

def open_chat(user_name):
    status = 'Online'
    sg.theme('LightGrey6') # give our window a spiffy set of colors

    layout = [[sg.MLine(size=(100, 20),key='-OUTPUT-', disabled=True, autoscroll=True, reroute_stdout=True, write_only=True, reroute_cprint=True)], 
            [sg.Input(size=(75, 1), key='-QUERY-', do_not_clear=True),
            sg.Button('SEND', bind_return_key=True),
            sg.B('Start A Thread')]]

    window = sg.Window(
        f'ChatNet: :{status}',
        layout, 
        font=('Helvetica', ' 13'), 
        default_button_element_size=(10, 1),
        finalize=True
        )

    while True:     # The Event Loop 
        event, value = window.read()            
        ts = dt.now()

        if event in (None, 'EXIT'):      
            break

        if event == 'SEND':
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            query = value['-QUERY-'].rstrip()
            cur.execute(f'''INSERT INTO chat_log(user, time, msg) VALUES('{user_name}','{ts}','{query.replace("'","`")}')''')
            conn.commit()
            conn.close()
            update_file(service)
            log = refresh_chat()
            window['-OUTPUT-'].update(log)
            window.find_element('-QUERY-').update('')
        if event.startswith('Start'):
            threading.Thread(target=the_thread, args=(window,), daemon=True).start()
        if event == '-THREAD-':
            window['-OUTPUT-'].update(refresh_chat())
           
            

        
            