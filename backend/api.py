from fastapi import FastAPI, File
from ultralytics import YOLO
from PIL import Image
import io
import json

app = FastAPI()
model = YOLO('best.pt')

@app.post("/predict", tags= ["Detector Endpoint"])
async def image_pred(file: bytes = File(...)):
    picture = Image.open(io.BytesIO(file), formats=None)
    results = model(picture)
    res_plotted = results[0].plot()
    res_plotted_rgb = res_plotted[:, :, ::-1]
    return json.dumps(res_plotted_rgb.tolist())