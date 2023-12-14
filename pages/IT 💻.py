import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from Home import matrix
import pandas as pd

SECTOR_INDEX = 2

# Initialize session state
if "target_index" not in st.session_state:
    st.session_state["target_index"] = 0
if "selected_service" not in st.session_state:
    st.session_state["selected_service"] = None
if "current_video_index" not in st.session_state:
    st.session_state["current_video_index"] = 0

print("Target index: ", st.session_state.target_index)


servizi = [row[SECTOR_INDEX] for row in matrix if row[3] != '' or row[SECTOR_INDEX] != '']

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

# Create buttons for each service inside the container
for index, servizio in enumerate(servizi):
    button_key = f"{servizio}_{index}"  # Unique key for each button
    if button_container[index].button(servizio, key=button_key):
        st.session_state.selected_service = servizio
        st.session_state.current_video_index = 0
        st.experimental_rerun()

if(st.session_state.selected_service != None):
    # Create next and previous buttons
    st.write("*Clicca su questi bottoni per navigare tra i video*")

    button_container2 = st.columns(4)

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

    # Button and input to jump to a specific video
    st.session_state.videos_map = {}
    num_videos = 0
    for row in data:
        if st.session_state.selected_service != None and len(row) >= 3 and row[1].lower() == st.session_state.selected_service.lower() and row[2] == "tenere":
            num_videos += 1
            st.session_state.videos_map[num_videos] = row[0]

    pd.set_option('display.max_colwidth', None)
    st.session_state.videos_df = pd.DataFrame(st.session_state.videos_map.items(), columns=["Numero", "Formazione"])
    st.write(st.session_state.videos_df)

    input_index = button_container2[2].number_input("Inserisci l'indice del video", min_value = 1, max_value = num_videos)
    st.session_state.target_index = input_index - 1
    jump_button = button_container2[3].button("Vai al video ⏯️")

    if jump_button:
        st.session_state.current_video_index = st.session_state.target_index
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
