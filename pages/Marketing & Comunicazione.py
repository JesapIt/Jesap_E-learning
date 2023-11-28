import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import IPython

servizi = ["SEO User Generated Content", "Marketing plan", "Event Management", "Social media Management", "Piano di comunicazione integrato", "Employer Branding"]
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
    if len(row) >= 3 and row[1].lower() == servizio.lower() and row[2] == "tenere":
        st.markdown(f"<h1 style='text-align: center; font-size: 36px; color: #983c8e;'>{row[0]}</h1>", unsafe_allow_html=True)
        if(row[4] == ""):
            st.error("La formazione " +  row[0] + " non è ancora disponibile")
        else:
            st.video(row[4])



