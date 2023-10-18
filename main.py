import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

st.set_page_config(layout="wide")
st.title("Scegli il servizio dalla barra laterale")
# def login_with_service_account():
#     settings = {
#                 "client_config_backend": "service",
#                 "service_config": {
#                     "client_json_file_path": "service-secrets.json",
#                 }
#             }
#     # Create instance of GoogleAuth
#     gauth = GoogleAuth(settings=settings)
#     # Authenticate
#     gauth.ServiceAuth()
#     return gauth


# gauth = login_with_service_account()
# drive = GoogleDrive(gauth)

# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
#          'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']

# creds = ServiceAccountCredentials.from_json_keyfile_name('service-secrets.json', scope)
# client = gspread.authorize(creds)
# link_data = "https://docs.google.com/spreadsheets/d/1AH776Bb55ZXRiFxoDi5-q_IQLhADW4pnNp4Rk2YlRlM/edit#gid=0"
# sht = client.open_by_url(link_data)
# worksheet = sht.worksheet("AUDIT")

# @st.cache_data 
# def get_data(_foglio):
#     data = []
#     try:
#         data = worksheet.get_all_values()
#         row_to_delete = ["NOME", "LINK"]
#         index_to_delete = data.index(row_to_delete)
#         data.pop(index_to_delete)
#     except:
#         print("nessun video")
#     return data

# data = get_data(worksheet)


# for row in data:
#     st.header(row[1])
#     st.caption(row[0])
#     st.video(row[2])

# st.markdown("link al foglio https://drive.google.com/drive/folders/1gSgIXqa9u9a9RckeZzEPezi5v_GRKQFx")


# folder_id = "1gSgIXqa9u9a9RckeZzEPezi5v_GRKQFx"

# query_str = "\'" + folder_id + "\'" + " in parents and trashed=false"    

# file_list = drive.ListFile({'q': query_str}).GetList()
# for file in file_list:
#     st.write('title: %s, id: %s' % (file['title'], file['id']))
#     video_url = "https://drive.google.com/uc?id=" + file['id']
#     st.video(video_url)
