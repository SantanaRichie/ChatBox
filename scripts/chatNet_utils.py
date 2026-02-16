#!/usr/bin/env python
from __future__ import print_function

import PySimpleGUI as sg
import hashlib
import yaml
import json
import os.path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from apiclient import errors
from googleapiclient.http import MediaFileUpload



def check_cred(usr, pwd, attempt):
    ''' 
    Check User provided Credentials against cred.yml
    Making sure access is Granted to Google Drive
    '''
    creds, service = get_drive_access()

    with open(r'C:\Users\richa\Documents\Work\DriveChat\configs\cred.yml', 'r') as c:
        file = yaml.safe_load(c)
        try:
            name = hashlib.md5(usr).hexdigest()
            pash = hashlib.md5(pwd).hexdigest()

            if file['user'][name] == pash:
                access = 'Granted'
                get_db(service=service)

                return access
        except KeyError as ke:

            error_msg = f'Credentials Do Not Match Any DriveChat User'
            attempt += 1
            access = get_cred(attempt, error_msg)[0]

            if access == 'Granted':
                get_db(service=service)
                return access


def get_cred(attempt=0, msg=None):
    '''
        Get credentials from user
    '''
    if attempt < 4:
        user_name = sg.popup_get_text(f'{msg} Retry: {attempt}\n User Name:')
        user_password = sg.popup_get_text('Password:', password_char='*')

        access = check_cred(user_name.encode('utf-8'),
                            user_password.encode('utf-8'), attempt)

    return access, user_name


def get_drive_access():
    '''
    Access Google API to google Drive
    '''
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('configs/token.json'):
        creds = Credentials.from_authorized_user_file('configs/token.json', SCOPES)
    else:
        print(f'No token available')

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # If the credentials are present but expired and a refresh token is available, attempt to refresh the credentials
            creds.refresh(Request())
        else:
            # If there is no refresh token, initiate OAuth 2.0 flow using client secret in credentials.json 
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\richa\Documents\Work\DriveChat\configs\credentials.json', SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open('configs/token.json', 'w') as token:
            token.write(creds.to_json())
            
    service = build('drive', 'v3', credentials=creds)
    return creds, service


def get_db(service):
    try:
        # get .db file id from .json if it exists and retreve .db from g drive
        if os.path.exists('configs/continued_chat.json'):
            print(f'configs/continued_chat.json exists {os.path.exists("configs/continued_chat.json")}')

            with open('configs/continued_chat.json', 'r') as f:
                pickup_id= json.load(f)['file_id']

            request = service.files().get_media(fileId=pickup_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f'Downloading chat.db from gdrive...')

            print('overwrite local chat.db with gdrive chat.db')    
            with open("configs/chat.db", "wb") as f:
                f.write(file.getvalue())
        else:
            fresh_chat = True
            raise Exception('missing continue chat file, starting fresh chat')
        
    except (Exception, HttpError) as error:
        # if db file doesn't exist create one
        if  (type(error) == HttpError and error.status_code == 404 ) or fresh_chat:
            print('.db file could not be found or starting a new chat log, previous log is deleted') 
            from db import create_chat_log
            create_chat_log()
            update_file(service, export_only=True)
        else:
            print(f'An error occurred: {error.status_code}')
            print(f'request retuned {request}')
  

def update_file(service, file_id=None, export_only=False, delete_only=False):
    # get file_id from continued_chat.json
    if os.path.exists('configs/continued_chat.json'):
        with open('configs/continued_chat.json', 'r') as f:
            file_id= json.load(f)['file_id']

    if not export_only:
        print('deleting')
        # Delete file upstream
        try:
            service.files().delete(fileId=file_id).execute()
        except errors.HttpError as error:
            print(f'An error occurred: {error}')

    if not delete_only:
        print('exporting')
        # Export local to replace deleted upstream file
        try:

            file_metadata = {
                'name': 'chat.db',
                'mimeType': 'application/vnd.sqlite3'
            }
            media = MediaFileUpload('configs/chat.db', mimetype='application/vnd.sqlite3',
                                    resumable=False)
            
            # create file on gdrive
            file = service.files().create(body=file_metadata, media_body=media,
                                            fields='id').execute()
            

            print(f'File with ID: "{file.get("id")}" has been uploaded.')

            #create continue chat json
            data = {'file_name': 'chat.db', 'file_id': file.get("id")}
            with open('configs/continued_chat.json','w') as out_file:
                json.dump(data,out_file)

        except HttpError as error:
            print(f'An error occurred: {error}')
            file = None
        print(file.get('id'))
        return file.get('id')


    

# def copy_db(creds, service, file_id = None):
#     copied_file = {'title': 'chat.db'}
#     try:
#         service = build('drive', 'v3', credentials=creds)
#         return service.files().copy(
#             fileId=file_id, body=copied_file).execute()
#     except errors.HttpError as error:
#         print(error)
#     return None
    

# TODO: handle orphan .db files , search and distroy 
# def search_file():
#     """Search file in drive location"""
#     creds, service = get_drive_access()

#     try:
#         files = []
#         page_token = None
#         while True:
#             response = service.files().list(q="mimeType='application/vnd.sqlite3'",
#                                             spaces='drive',
#                                             fields='nextPageToken, '
#                                                    'files(id, name)',
#                                             pageToken=page_token).execute()
#             for file in response.get('files', []):
#                 # Process change
#                 print(F'Found file: {file.get("name")}, {file.get("id")}')
#             files.extend(response.get('files', []))
#             page_token = response.get('nextPageToken', None)
#             if page_token is None:
#                 break

#     except HttpError as error:
#         print(F'An error occurred: {error}')
#         files = None

#     return files

# search_file()