#!/usr/bin/env python
from chatNet_utils import get_cred
from chat_ui import open_chat
import PySimpleGUI as sg




if __name__ == '__main__':
    sg.theme('LightGrey 6')
    access, user_name = get_cred()
    if access == 'Granted':
        open_chat(user_name)