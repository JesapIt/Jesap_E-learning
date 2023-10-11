import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']

creds = ServiceAccountCredentials.from_json_keyfile_name('service-secrets.json', scope)
client = gspread.authorize(creds)
link_data = "https://docs.google.com/spreadsheets/d/1AH776Bb55ZXRiFxoDi5-q_IQLhADW4pnNp4Rk2YlRlM/edit#gid=0"
sht = client.open_by_url(link_data)
worksheet = sht.worksheet("IT")

@st.cache_data 
def get_data(_foglio):
    data = worksheet.get_all_values()
    row_to_delete = ["NOME", "LINK"]
    index_to_delete = data.index(row_to_delete)
    data.pop(index_to_delete)
    return data

data = get_data(worksheet)


for row in data:
    st.header(row[0])
    st.video(row[1])