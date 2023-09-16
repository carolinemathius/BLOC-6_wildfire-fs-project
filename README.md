# Wildfire Detection Application
Final project of data fullstack JEDHA's bootcamp
BLOC 6

[Presentation video](https://share.vidyard.com/watch/he67GRQXPZYmeKi6zXaBwH?)

## Description

Wildfire Detection is an application designed to help users identify and report wildfires quickly. Our application uses state-of-the-art computer vision and data analysis techniques to detect fire and smoke in images, providing crucial information to emergency services.

## Features

- **File Upload**: Users can upload images containing potential wildfire scenes.
- **Camera Input**: Users can use their phone's camera to capture and analyze images in real-time.
- **Fire and Smoke Detection**: Our application uses a custom-trained YOLOv8 model to detect fire and smoke in images.
- **Geolocation**: If available, the application displays the GPS coordinates of the image, helping emergency services locate the fire.
- **Weather Information**: Users can access weather data related to the detected fire's location, including wind speed and direction.
- **User-Friendly Interface**: The user interface is simple and intuitive, making it easy for anyone to use.

## Getting Started

To get started with Wildfire Detection on your local machine, follow these steps:

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Docker (optional)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/carolinemathius/wildfire-fs-project.git
   cd wildfire-fs-project
   ```

2. Set up the frontend and backend environments:

   - **Frontend**:

     ```bash
     cd frontend
     pip install -r requirements.txt
     ```

   - **Backend**:

     ```bash
     cd backend
     pip install -r requirements.txt
     ```

### Usage

1. Start the backend server:

   ```bash
   cd backend
   python api.py
   ```

   The API server will be running at `http://localhost:4001`.

2. Start the frontend application:

   ```bash
   cd frontend
   streamlit run streamlit.py
   ```

   The Streamlit application will open in your web browser.

3. Use the application to upload images or capture images with your phone's camera for wildfire detection.

## Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Make your changes and test them thoroughly.
4. Create a pull request with a clear description of your changes.

## Authors

- [Anas Maghous](https://www.linkedin.com/in/anas-maghous/)
- [Caroline Mathius](https://www.linkedin.com/in/carolinemathius/)
- [Simon Picard](https://www.linkedin.com/in/simon-p-64371968/)
- [Thibaut Longchamps](https://www.linkedin.com/in/thibaut-longchamps-0922525a/)

## Acknowledgments

We would like to thank the open-source community for providing the tools and libraries that made this project possible.

## References

We used the [D-Fire Dataset](https://github.com/gaiasd/DFireDataset), built by:
Pedro Vinícius Almeida Borges de Venâncio, Adriano Chaves Lisboa, Adriano Vilela Barbosa: An automatic fire detection system based on deep convolutional neural networks for low-power, resource-constrained devices. In: Neural Computing and Applications, 2022.

[API with our trained YOLOv8 model](https://wildfire-project-backend.herokuapp.com)\
[Streamlit app with our integrated fire&smoke detector for emergency services](https://wildfire-project-streamlit.herokuapp.com/)
