import streamlit as st
from utils import *

if __name__ == '__main__':

    # Set the configuration of the page
    st.set_page_config(layout='centered', page_title='Project Wildfire', page_icon='🔥')  

    # Create a sidebar on the page and create a select box to choose the detection method
    st.write("<h1 style='text-align: center;'>🔥 Project Wildfire 🔥</h1>", unsafe_allow_html=True)
    st.divider()
    st.subheader('Welcome to our Wildfire application! '
             'Please upload a picture in our app and test our model. '
             'If there is fire or smoke on your picture, '
             'our model will detect it, give back the GPS coordinates '
             'and give you some information about weather forecast '
             'to help the emergency services assess the situation.')
    st.divider()
    st.sidebar.header('Fire detection module') 
    option = st.sidebar.selectbox('Chose your detection method',('File upload', 'Phone camera'))

    # If the 'File upload' option is selected, create a file uploader 
    if option == 'File upload':
        my_upload = st.sidebar.file_uploader('Upload your file',type=["png", "jpg", "jpeg"], label_visibility = 'visible')

    # If the 'Phone camera' option is selected, create a camera input
    if option == 'Phone camera':
        my_upload = st.sidebar.camera_input('Take a picture')

    # If the file uploader or camera input returns a file, display the results of the detection model, the GPS coordinates and the weather information in separate containers
    if my_upload is not None:
        with st.container():
            st.header('💻 Results from our detection model')
            prediction(my_upload)
            st.divider()
        with st.container():
            st.header('📡 GPS coordinates')
            gps_map(my_upload)
            st.divider()
        with st.container():
            st.header('⛅ Weather informations')
            weather_info(my_upload)