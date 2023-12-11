import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread import Cell
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import IPython
from Home import matrix

if "target_index" not in st.session_state:
    st.session_state["target_index"] = 0
if "selected_service" not in st.session_state:
    st.session_state["selected_service"] = None
if "current_video_index" not in st.session_state:
    st.session_state["current_video_index"] = 0

servizi = [row[1] for row in matrix if row[0] != '']

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
    # Create an instance of GoogleAuth
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
st.write("*Scegli il servizio specifico cliccando sul bottone corrispondente*")
button_container = st.columns(len(servizi))
st.markdown("---")

# Create next and previous buttons
st.write("*Clicca su questi bottoni per navigare tra i video*")
button_container2 = st.columns(2)  # Create a container with 2 columns

prev_button = button_container2[0].button("Precedente ⏮️")
next_button = button_container2[1].button("Successivo ⏭️")

if prev_button:
    st.session_state.current_video_index -= 1
    if st.session_state.current_video_index < 0:
        st.session_state.current_video_index = 0
    st.experimental_rerun()

if next_button:
    st.session_state.current_video_index += 1
    st.experimental_rerun()

# Create buttons for each service inside the container
for index, servizio in enumerate(servizi):
    button_key = f"{servizio}_{index}"  # Unique key for each button
    if button_container[index].button(servizio, key=button_key):
        st.session_state.selected_service = servizio
        st.session_state.current_video_index = 0
        st.experimental_rerun()

st.markdown("---")

# Display video for the selected service and current video index
selected_service = st.session_state.selected_service
current_video_index = st.session_state.current_video_index

if selected_service is not None:
    st.title(f"{selected_service}")
    videos_found = 0
    for row in data:
        if len(row) >= 3 and row[1].lower() == selected_service.lower() and row[2] == "tenere":
            if videos_found == current_video_index:
                st.markdown(f"<h1 style='text-align: center; font-size: 36px; color: #983c8e;'>{row[0]}</h1>",
                            unsafe_allow_html=True)
                if row[4] == "":
                    st.error("La formazione " + row[0] + " non è ancora disponibile")
                else:
                    st.video(row[4])
                break
            videos_found += 1
    else:
        st.warning("Non ci sono altre formazioni per il servizio selezionato!")




