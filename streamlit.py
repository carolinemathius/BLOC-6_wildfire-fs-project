import streamlit as st
import folium
from PIL import Image, ExifTags
from streamlit_folium import st_folium

st.set_page_config(layout='wide', page_title='Project Wildfire')
st.title('Project Wildfire :fire:')

my_upload = st.file_uploader('Upload your picture here', type=["png", "jpg", "jpeg"])
col1, col2 = st.columns(2)

# Return GPS informations
def get_gps(image):
    data = dict()
    exif = image.getexif()
    if exif:
        # GPS Info
        ifd = exif.get_ifd(0x8825)
        for key, val in ifd.items():
            data[ExifTags.GPSTAGS[key]] = val
    lat =  data['GPSLatitudeRef'], data['GPSLatitude']
    long = data['GPSLongitudeRef'], data['GPSLongitude']
    latitude = degrees_to_decimals(lat)
    longitude = degrees_to_decimals(long)
    return latitude, longitude

# Display folium map
def display_map(coordinates):
    map = folium.Map(location=[coordinates[0], coordinates[1]], zoom_start=16)
    folium.Marker(
        [coordinates[0], coordinates[1]], popup="Picture location", tooltip="Picture location"
    ).add_to(map)
    st_folium(map, width=725,returned_objects=[])

# Convert GPS to decimals degrees
def degrees_to_decimals(geo_coord):
    direction =  geo_coord[0]
    degrees, minutes, seconds = [geo_coord[1][i] for i in range(3)]
    d_t_d = float(degrees) + float(minutes)/60 + float(seconds)/3600
    if direction in ('S','W'):
        d_t_d*= -1
    return d_t_d

# Display original uploaded image and GPS coordinates
def display_img_gps_location(upload):
    image = Image.open(upload)

    with col1:
        st.header('Original image')
        st.image(upload)
    
    with col2:
        st.header('Fire localisation')
        display_map(get_gps(image))
    
if my_upload is not None:
    display_img_gps_location(my_upload)