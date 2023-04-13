import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json
import numpy as np
from PIL import Image, ExifTags
from config import weather_api_url, weather_api_key, yolo_api_url

# api request to run the model and plot the predicted boxes/classes
def prediction(api_predict):
    files = {"file": api_predict}
    res = requests.post(url=yolo_api_url, files=files)
    res_array = np.asarray(json.loads(res.json()))
    return st.image(res_array, width=725, caption='YOLOv8 custom trained model prediction')

# convert GPS to decimals degrees
def gps_decimals(gps_degrees):
    direction, (degrees, minutes, seconds) = gps_degrees[0], gps_degrees[1]  # extract the direction and the degrees, minutes, seconds values
    decimals = float(degrees) + float(minutes) / 60 + float(seconds) / 3600  # calculate the decimal degree value
    if direction in ('S', 'W'):  # check if the direction is south or west and adjust the value accordingly
        decimals *= -1
    return decimals

# retrieve gps data from file's exif, return False if not found
def gps_data(uploaded_photo):
    image = Image.open(uploaded_photo)
    data = dict()
    exif = image.getexif()  
    if exif:
        ifd = exif.get_ifd(0x8825)  
        for key, val in ifd.items():
            data[ExifTags.GPSTAGS[key]] = val  
    if 'GPSLatitudeRef' in data:
        gps_coordinates = gps_decimals((data['GPSLatitudeRef'], data['GPSLatitude'])), gps_decimals((data['GPSLongitudeRef'], data['GPSLongitude'])) 
        return gps_coordinates
    else:
        return False

# if GPS data is available, create and display a folium map centered on the GPS coordinates, add a marker on the map     
def gps_map(uploaded_photo):
    if gps_data(uploaded_photo) is not False:
        coordinates = gps_data(uploaded_photo)
        map = folium.Map(location=coordinates, zoom_start=16)  
        folium.Marker(coordinates, popup="Fire location", tooltip="Fire location").add_to(map)  
        st_folium(map, width=725, returned_objects=[])  
    else :
        st.subheader('No GPS coordinates found on the provided photo.')
        st.subheader('Please ensure that your photo gps location is activated on your device.')

# if GPS data is available, call an openweather api, display information related to the wind
def weather_info(uploaded_photo):
    if gps_data(uploaded_photo) is not False:
        coordinates = gps_data(uploaded_photo)
        response = requests.get(weather_api_url.format(str(coordinates[0]), str(coordinates[1]), weather_api_key))
        weather_data = json.loads(response.text)
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
        st.subheader('No weather informations are available.')