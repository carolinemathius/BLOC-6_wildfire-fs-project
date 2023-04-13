import streamlit as st
from utils import *

def processing(my_upload):
    if my_upload is not None:
        with st.container():
            prediction(my_upload)
        with st.container():
            gps_map(my_upload)
        with st.container():
            weather_info(my_upload)



# main program
if __name__ == '__main__':

    st.set_page_config(layout='centered', page_title='Project Wildfire', page_icon='🔥')  
    st.title('Project Wildfire')
    st.sidebar.header('Fire detection module')
    option = st.sidebar.selectbox('Chose your detection method',('File upload', 'Phone camera'))
    if option == 'File upload':
        my_upload = st.sidebar.file_uploader('Upload your file',type=["png", "jpg", "jpeg"], label_visibility = 'visible')
    if option == 'Phone camera':
        my_upload = st.sidebar.camera_input('Take a picture')
    st.sidebar.button("Detect", on_click = processing(my_upload))  
