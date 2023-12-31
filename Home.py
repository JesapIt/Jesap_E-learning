import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
st.title("Scegli la sezione desiderata dalla barra laterale 🗺️")
st.write("Ogni colonna presenta i servizi offerti per la sezione selezionata.")

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


cells = worksheet.range('G5:J5')

values = [cell.value for cell in cells]
cells = worksheet.range('G6:J15')
matrix = []
for i in range(5):
    row = []
    for j in range(4):
        row.append(cells[i*4+j].value)
    matrix.append(row)

df = pd.DataFrame(matrix, columns=[values[0], values[1], values[2], values[3]])
st.write(df)


# Define two columns
col1, col2, col3 = st.columns(3)

# Add markdown to the second column
with col3:
    st.markdown("""
        <head>
        <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body><br><br>
        <div class="mioDiv" style="text-align: left;">
        <img src="https://jesap.it/wp-content/uploads/2023/03/4-scaled.webp" width="250">
        <p>Powered by <a href="https://jesap.it">Jesap Consulting</a></p>
        <p>Per assistenza tecnica: <a href="it@jesap.it">it@jesap.it</a></p>
        </div>
        </body>
        """, unsafe_allow_html=True)



