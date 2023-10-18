import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

st.set_page_config(layout="wide")
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

folder_id = ""

query_str = "\'" + folder_id + "\'" + " in parents and trashed=false"    

file_list = drive.ListFile({'q': query_str}).GetList()
for file in file_list:
    st.write('title: %s, id: %s' % (file['title'], file['id']))
    video_url = "https://drive.google.com/uc?id=" + file['id']
    st.video(video_url)