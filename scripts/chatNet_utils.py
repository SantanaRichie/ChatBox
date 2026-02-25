#!/usr/bin/env python
import hashlib
import yaml
import customtkinter as ctk


def check_cred(usr, pwd, attempt):
    """Check user credentials against cred.yml"""
    with open(r'configs\cred.yml', 'r') as c:
        file = yaml.safe_load(c)
        try:
            name = hashlib.md5(usr).hexdigest()
            pash = hashlib.md5(pwd).hexdigest()

            if file['user'][name] == pash:
                return 'Granted'
        except KeyError:
            return 'Credentials Do Not Match Any ChatBox User'


def get_cred(attempt=0, msg=None):
    """Get credentials from user using GUI"""
    while attempt < 4:
        root = ctk.CTk()
        root.title("Login")
        root.geometry("400x300")
        
        frame = ctk.CTkFrame(root)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        if msg:
            ctk.CTkLabel(frame, text=f'{msg} Retry: {attempt}', text_color="red").pack(pady=5)
        
        ctk.CTkLabel(frame, text="User Name:").pack(pady=5)
        user_entry = ctk.CTkEntry(frame, width=200)
        user_entry.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Password:").pack(pady=5)
        password_entry = ctk.CTkEntry(frame, width=200, show="*")
        password_entry.pack(pady=5)
        
        result = {'user_name': None, 'access': None}
        
        def submit():
            user_name = user_entry.get()
            user_password = password_entry.get()
            access = check_cred(user_name.encode('utf-8'), user_password.encode('utf-8'), attempt)
            result['user_name'] = user_name
            result['access'] = access
            root.destroy()
        
        ctk.CTkButton(frame, text="Login", command=submit).pack(pady=20)
        root.mainloop()
        
        if result['access'] == 'Granted':
            return result['access'], result['user_name']
        
        attempt += 1
        msg = result['access'] if result['access'] else 'Invalid credentials'
    
    return None, None
