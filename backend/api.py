from fastapi import FastAPI, File
from fastapi.responses import RedirectResponse
from ultralytics import YOLO
from PIL import Image
import io
import json
import uvicorn

description = """
Welcome to Wildfire_Project api 

## Introduction endpoint

* `/`: **GET** request that simply redirects to API documentation. 

## Detector endpoint

* `/image-detector`: **POST** request that runs the Wildfire detection model on uploaded image and outputs the result. 

Check out documentation below 👇 for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Introduction Endpoint",
        "description": "Redirect to documentation"
    },

    {
        "name": "Detector Endpoint",
        "description": "Wildfire Predictor"
    }
]


app = FastAPI(
    title="🔥 Wildfire Project API",
    description=description,
    version="0.1",
    contact={
        "name": "Wildfire",
        "url": "https://wildfire-streamlit.herokuapp.com/",
    },
    openapi_tags=tags_metadata
)

model = YOLO('best.pt')    # Load trained model


@app.get("/", tags= ["Introduction Endpoint"])
async def docs_redirect():
    """
    Simply redirects to /docs

    """
    return RedirectResponse(url='/docs')

@app.post("/predict", tags= ["Detector Endpoint"])
async def image_pred(file: bytes = File(...)):
    """
    Make image prediction
    """
    picture = Image.open(io.BytesIO(file), formats=None) # Open bytes image received in PIL format
    results = model(picture) # Load PIL image in model
    res_plotted = results[0].plot() # Loaded image with detected bounding boxes in numpy array format https://docs.ultralytics.com/modes/predict/#probs
    res_plotted_rgb = res_plotted[:, :, ::-1] # Convert from BGR colors to RGB
    return json.dumps(res_plotted_rgb.tolist()) # Send np.array serialized into JSON object 



if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4001) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)