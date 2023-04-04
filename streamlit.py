import streamlit as st
from exif import Image
from io import BytesIO 


st.set_page_config(layout='centered', page_title='Project Wildfire')
st.title('Project Wildfire :fire:')

picture_bytes = st.file_uploader('Upload your picture here', type=["png", "jpg", "jpeg"])


def image_gps_location(picture):
    latitude = picture.gps_latitude
    longitude = picture.gps_longitude
    return latitude

if picture_bytes is not None:
    picture_upload = Image.open(picture_bytes)
    with open(picture_upload, 'rb') as image_file:
        picture = Image(image_file)
    image_gps_location(picture_upload)