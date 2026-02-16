#!/usr/bin/env python
from chatNet_utils import get_cred
from chat_ui import open_chat
import customtkinter as ctk

# application starts here

if __name__ == '__main__':
    ctk.set_appearance_mode("Light")
    access, user_name = get_cred()
    if access == 'Granted':
        open_chat(user_name)