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
from Home import matrix

# Condividi matrix della Home.py con AUDIT.py e altri per creare bottoni

servizi = [row[3] for row in matrix if row[3] != '']
st.write("Scegli il servizio specifico cliccando sul bottone corrispondente")
# servizi = ["Automazione dei processi", "Business Intelligence"]
# servizio = st.selectbox("Scegli il servizio specifico", servizi)

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


# Create a container to hold the buttons in a single row
button_container = st.columns(len(servizi))

# Create buttons for each service inside the container
for index, servizio in enumerate(servizi):
    button_key = f"{servizio}_{index}"  # Unique key for each button
    if button_container[index].button(servizio, key=button_key):
        # Your existing code for handling the selected service goes here
        # For example, you can replace the st.selectbox code with your logic
        st.title(f"{servizio}")

        for row in data:
            if len(row) >= 3 and row[1].lower() == servizio.lower() and row[2] == "tenere":
                st.markdown(f"<h1 style='text-align: center; font-size: 36px; color: #983c8e;'>{row[0]}</h1>", unsafe_allow_html=True)
                if(row[4] == ""):
                    st.error("La formazione " +  row[0] + " non è ancora disponibile")
                else:
                    st.video(row[4])




