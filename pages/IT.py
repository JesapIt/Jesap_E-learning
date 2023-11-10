import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import IPython

servizi = ["E-Commerce", "Sviluppo di Web App", "Creazione di software CRM/ERM"]
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

for row in data:
    if row[1].lower() == servizio.lower() and row[2] == "tenere":
        st.write("Titolo:", row[0])
        



