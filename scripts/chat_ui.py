import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime as dt
import sqlite3
import time
import threading
from chatNet_utils import get_drive_access, update_file

path = r'C:\Users\richa\Documents\Work\DriveChat\configs\chat.db'

def the_thread(window):
    """
    The thread that communicates with the application through the window's events.

    Once a second wakes and sends a new event and associated value to the window
    """
    i = 0
    while True:
        time.sleep(5)
        window.after(0, update_chat_display)
        i += 1

def refresh_chat(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('Select time, user, msg From chat_log Order by time asc')
    res = cur.fetchall()
    log = ''.join([f'{entry[0]}: {entry[1]}- {entry[2]}\n' for entry in res])
    conn.close()
    return log

def open_chat(user_name):
    status = 'Online'
    ctk.set_appearance_mode("Light")
    
    # Get Google Drive access after successful login
    creds, service = get_drive_access()
    
    root = ctk.CTk()
    root.title(f'ChatNet: {status}')
    root.geometry("800x600")
    
    # Main frame
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Chat display area
    chat_display = ctk.CTkTextbox(main_frame, height=400, wrap="word")
    chat_display.pack(fill="both", expand=True, padx=5, pady=5)
    chat_display.configure(state="disabled")
    
    # Input frame
    input_frame = ctk.CTkFrame(main_frame)
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Message input
    message_entry = ctk.CTkEntry(input_frame, placeholder_text="Type your message...")
    message_entry.pack(side="left", fill="x", expand=True, padx=5)
    
    # Send button
    send_button = ctk.CTkButton(input_frame, text="SEND", command=lambda: send_message())
    send_button.pack(side="right", padx=5)
    
    # Thread button
    thread_button = ctk.CTkButton(input_frame, text="Start A Thread", command=start_thread)
    thread_button.pack(side="right", padx=5)
    
    def send_message():
        query = message_entry.get().strip()
        if query:
            ts = dt.now()
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            cur.execute(f"""INSERT INTO chat_log(user, time, msg) VALUES('{user_name}','{ts}','{query.replace("'","`")}')""")
            conn.commit()
            conn.close()
            
            update_file(service)
            message_entry.delete(0, 'end')
            update_chat_display()
    
    def update_chat_display():
        log = refresh_chat(path)
        chat_display.configure(state="normal")
        chat_display.delete('1.0', 'end')
        chat_display.insert('1.0', log)
        chat_display.configure(state="disabled")
        chat_display.see('end')
    
    def start_thread():
        threading.Thread(target=the_thread, args=(root,), daemon=True).start()
    
    # Bind Enter key to send message
    message_entry.bind('<Return>', lambda event: send_message())
    
    # Initial chat display update
    update_chat_display()
    
    root.mainloop()