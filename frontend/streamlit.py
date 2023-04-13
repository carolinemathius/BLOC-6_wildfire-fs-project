import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json
import numpy as np
from PIL import Image, ExifTags
from config import weather_api_key, yolo_api_url


# convert GPS to decimals degrees
def gps_decimals(gps_degrees):
    direction, (degrees, minutes, seconds) = gps_degrees[0], gps_degrees[1]  # extract the direction and the degrees, minutes, seconds values
    decimals = float(degrees) + float(minutes) / 60 + float(seconds) / 3600  # calculate the decimal degree value
    if direction in ('S', 'W'):  # check if the direction is south or west and adjust the sign accordingly
        decimals *= -1
    return decimals

# api request to run the model and plot the predict boxes
def prediction(api_predict):
    files = {"file": api_predict}
    res = requests.post(url=yolo_api_url, files=files)
    res_array = np.asarray(json.loads(res.json()))
    return st.image(res_array, width=725)

def gps_data(uploaded_photo):
    image = Image.open(uploaded_photo)
    data = dict()
    exif = image.getexif()  # get the EXIF data from the image
    if exif:
        ifd = exif.get_ifd(0x8825)  # retrieve the GPS EXIF data
        for key, val in ifd.items():
            data[ExifTags.GPSTAGS[key]] = val  # extract the GPS information from the EXIF data

    if 'GPSLatitudeRef' in data:
        coordinates = gps_decimals((data['GPSLatitudeRef'], data['GPSLatitude'])), gps_decimals((data['GPSLongitudeRef'], data['GPSLongitude']))  # convert the GPS coordinates to decimal degrees
        map = folium.Map(location=coordinates, zoom_start=16)  # create a folium map centered on the GPS coordinates
        folium.Marker(coordinates, popup="Fire location", tooltip="Fire location").add_to(map)  # add a marker to the map at the GPS coordinates
        st_folium(map, width=725)  # display the map using the Streamlit-Folium bridge

        response = requests.get('https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(str(coordinates[0]), str(coordinates[1]), weather_api_key))
        weather_data = json.loads(response.text)
        st.subheader('Wind speed : {} km/h.'.format(weather_data['wind']['speed']))
        st.subheader('Wind direction : {} degrees.'.format(weather_data['wind']['deg']))
        st.subheader('Wind gust : {} km/h.'.format(weather_data['wind']['gust']))
    
    else:
        st.subheader('No GPS coordinates found on provided picture')
        st.subheader('No weather information available')


# main program
if __name__ == '__main__':

    st.set_page_config(layout='wide', page_title='Project Wildfire')  
    st.title('Project Wildfire :fire:')
    st.sidebar.write('Fire detection module')
    my_upload = st.sidebar.file_uploader('Upload your picture here', type=["png", "jpg", "jpeg"])  
    col1, col2 = st.columns(2)
    if my_upload is not None:
        with col1:  
            prediction(my_upload)
        with col2:
            gps_data(my_upload)

