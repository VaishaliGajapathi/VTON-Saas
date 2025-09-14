import os, uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import boto3
from shap_e.models.download import load_model
from shap_e.util.notebooks import save_glb
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# AWS S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
BUCKET = os.getenv("S3_BUCKET_NAME")

# Load Hugging Face model
model = load_model(os.getenv("HF_MODEL_NAME"))

@app.post("/generate-3d")
async def generate_3d(file: UploadFile = File(...)):
    # Save uploaded image temporarily
    temp_image_path = f"/tmp/{uuid.uuid4()}.png"
    with open(temp_image_path, "wb") as f:
        f.write(await file.read())

    # Generate 3D model
    output_glb_path = f"/tmp/{uuid.uuid4()}.glb"
    mesh = model.generate(file_path=temp_image_path)  # adjust to your model's API
    save_glb(mesh, output_glb_path)

    # Upload to S3
    s3_key = f"models/{uuid.uuid4()}.glb"
    s3.upload_file(output_glb_path, BUCKET, s3_key, ExtraArgs={"ContentType": "model/gltf-binary"})

    s3_url = f"https://{BUCKET}.s3.amazonaws.com/{s3_key}"
    return JSONResponse({"model_url": s3_url})
