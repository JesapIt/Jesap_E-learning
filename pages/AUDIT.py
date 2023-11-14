import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import IPython
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
import streamlit as st
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow

servizi = ["Automazione dei processi", "Business Intelligence"]
servizio = st.selectbox("Scegli il servizio specifico", servizi)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']

creds = ServiceAccountCredentials.from_json_keyfile_name('service-secrets.json', scope)
client = gspread.authorize(creds)

def login_with_service_account():
    settings = {
                "client_config_backend": "service",
                "service_config": {
                    "client_json_file_path": "service-secrets.json",
                }
            }
    # Create instance of GoogleAuth
    gauth = GoogleAuth(settings=settings)
    # Authenticate
    gauth.ServiceAuth()
    return gauth


gauth = login_with_service_account()
drive = GoogleDrive(gauth)

link_data = "https://docs.google.com/spreadsheets/d/1ZD2ij7KSPJ4rAhfrqc5w3EMGPksaqrAqbeKPLHRrR80/edit#gid=0"
sht = client.open_by_url(link_data)

worksheet = sht.sheet1
data = worksheet.get_all_values()

CLIENT_ID = '615937050302-90srrtrnao4pliqjlfcem2t7tcimo94a.apps.googleusercontent.com'
CLIENT_SECRET = 'GOCSPX-YDEmo3zeaTIJZVFSS96VCjyq7DdY'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Authenticate the user and obtain credentials
flow = InstalledAppFlow.from_client_secrets_file("pages\google-secrets.json", scopes=SCOPES)
credentials = flow.run_local_server(port=0)
youtube = build('youtube', 'v3', credentials=credentials)
'''
for row in data:
    if len(row) >= 3 and row[1].lower() == servizio.lower() and row[2] == "tenere":
        st.markdown(f"<h1 style='text-align: center; font-size: 36px;'>{row[0]}</h1>", unsafe_allow_html=True)
        try:
            video_id = 'aNJDQq6yYxI'
            video_response = youtube.videos().list(part='player', id=video_id).execute()
            video_url = video_response['items'][0]['player']['embedHtml']
            st.markdown(video_url, unsafe_allow_html=True)
        except HttpError as e:
            st.error(f'An error occurred: {e}')
'''



