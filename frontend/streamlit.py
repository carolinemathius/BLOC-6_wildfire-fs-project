import streamlit as st
from utils import *

if __name__ == '__main__':

    # Set the configuration of the page
    st.set_page_config(layout='centered', page_title='Project Wildfire', page_icon='🔥')  

    # Create a sidebar on the page and create a select box to choose the detection method
    st.write("<h1 style='text-align: center;'>🔥 Project Wildfire 🔥</h1>", unsafe_allow_html=True)
    with st.sidebar:
        st.header('Fire detection module') 
        option = st.selectbox('Chose your detection method',('File upload', 'Phone camera'))

        # If the 'File upload' option is selected, create a file uploader 
        if option == 'File upload':
            my_upload = st.file_uploader('Upload your file',type=["png", "jpg", "jpeg"], label_visibility = 'visible')

        # If the 'Phone camera' option is selected, create a camera input
        if option == 'Phone camera':
            my_upload = st.camera_input('Take a picture')
        st.divider()
        st.markdown('Welcome to our Wildfire application!')
        st.markdown('Please upload a picture in our app and test our model. '
                    'If there is fire or smoke on your picture, '
                    'our model will detect it.')
        st.markdown('If there are exploitable exif data on your picture, '
                    'our application will display the gps location as well as '
                    'wind related weather, to potentially '
                    'help emergency services assess the situation.')
        st.divider()
        st.markdown('**Wildfire project by :**')
        st.markdown('[_Anas Maghous_](%s)'%'https://www.linkedin.com/in/anas-maghous/')
        st.markdown('[_Caroline Mathius_](%s)'%'https://www.linkedin.com/in/carolinemathius/')
        st.markdown('[_Simon Picard_](%s)'%'https://www.linkedin.com/in/simon-p-64371968/')
        st.markdown('[_Thibaut Longchamps_](%s)'%'https://www.linkedin.com/in/thibaut-longchamps-0922525a/')
        st.divider()
        st.markdown('[**Link to our Github**](%s)'%'https://github.com/carolinemathius/wildfire-fs-project')

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

# Remove Made with Streamlit footer and top right burger menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 