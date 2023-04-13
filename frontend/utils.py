import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json
import numpy as np
from PIL import Image, ExifTags
from config import weather_api_url, weather_api_key, yolo_api_url

# api request to run the model and plot the predict boxes
def prediction(api_predict):
    files = {"file": api_predict}
    res = requests.post(url=yolo_api_url, files=files)
    res_array = np.asarray(json.loads(res.json()))
    return st.image(res_array, width=725, caption='YOLOv8 custom trained model prediction')

# convert GPS to decimals degrees
def gps_decimals(gps_degrees):
    direction, (degrees, minutes, seconds) = gps_degrees[0], gps_degrees[1]  # extract the direction and the degrees, minutes, seconds values
    decimals = float(degrees) + float(minutes) / 60 + float(seconds) / 3600  # calculate the decimal degree value
    if direction in ('S', 'W'):  # check if the direction is south or west and adjust the sign accordingly
        decimals *= -1
    
    return decimals

def gps_data(uploaded_photo):
    image = Image.open(uploaded_photo)
    data = dict()
    exif = image.getexif()  # get the EXIF data from the image
    if exif:
        ifd = exif.get_ifd(0x8825)  # retrieve the GPS EXIF data
        for key, val in ifd.items():
            data[ExifTags.GPSTAGS[key]] = val  # extract the GPS information from the EXIF data
    if 'GPSLatitudeRef' in data:
        gps_coordinates = gps_decimals((data['GPSLatitudeRef'], data['GPSLatitude'])), gps_decimals((data['GPSLongitudeRef'], data['GPSLongitude']))  # convert the GPS coordinates to decimal degrees
        return gps_coordinates
    else:
        return False
    
def gps_map(uploaded_photo):
        if gps_data(uploaded_photo) is not False:
            coordinates = gps_data(uploaded_photo)
            map = folium.Map(location=coordinates, zoom_start=16)  # create a folium map centered on the GPS coordinates
            folium.Marker(coordinates, popup="Fire location", tooltip="Fire location").add_to(map)  # add a marker to the map at the GPS coordinates
            st_folium(map, width=725)  # display the map using the Streamlit-Folium bridge
        else :
            st.subheader('No GPS coordinates found on provided picture')

def weather_info(uploaded_photo):
        if gps_data(uploaded_photo) is not False:
            coordinates = gps_data(uploaded_photo)
            response = requests.get(weather_api_url.format(str(coordinates[0]), str(coordinates[1]), weather_api_key))
            weather_data = json.loads(response.text)
            st.header('Wind information at GPS point : ')
            if 'speed' in weather_data['wind']:
                st.subheader('Wind speed : {} km/h.'.format(weather_data['wind']['speed']))
            else:
                st.subheader('No wind speed information available')                
            if 'deg' in weather_data['wind']:
                st.subheader('Wind direction : {} degrees.'.format(weather_data['wind']['deg']))
            else:
                st.subheader('No wind direction information available')
            if 'gust' in weather_data['wind']:
                st.subheader('Wind gust : {} km/h.'.format(weather_data['wind']['gust']))
            else:
                st.subheader('No wind gust information available')
        else:
            st.subheader('No weather information available')