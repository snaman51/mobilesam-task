from fastapi import FastAPI, File, UploadFile, HTTPException
from main import segment_everything
import io
import os
from fastapi.responses import FileResponse
from PIL import Image


app = FastAPI()

output_path = "generated/"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
@app.post("/segment-image")
async def segment_image(file: UploadFile):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    try:
        segmentation_result = segment_everything(image=image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segmentation failed: {str(e)}")

    try:
        output_file_path = os.path.join(output_path, "output.png")
        segmentation_result.save(output_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save segmented image: {str(e)}")

    return FileResponse(path=output_file_path, media_type='image/png', filename='output.png')
