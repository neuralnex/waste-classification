from fastapi import FastAPI, File, UploadFile, HTTPException
from transformers import pipeline
from PIL import Image
import io

app = FastAPI(
    title="Waste Classification API",
    description="AI-powered waste classification using SigLIP2",
    version="1.0.0"
)

# Load model once when the application starts
classifier = pipeline(
    "image-classification",
    model="prithivMLmods/Augmented-Waste-Classifier-SigLIP2"
)

# Map the model's 10 classes to our 2 categories
CATEGORY_MAP = {
    "Battery": "recyclable",
    "Biological": "biological",
    "Cardboard": "recyclable",
    "Clothes": "recyclable",
    "Glass": "recyclable",
    "Metal": "recyclable",
    "Paper": "recyclable",
    "Plastic": "recyclable",
    "Shoes": "recyclable",
    "Trash": "recyclable",
}


@app.get("/")
def root():
    return {
        "message": "Waste Classification API",
        "status": "running"
    }


@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    # Validate image type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image."
        )

    try:
        # Read uploaded image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Run classification
        predictions = classifier(image)

        # Get highest-confidence prediction
        best_prediction = predictions[0]

        detected_type = best_prediction["label"]
        confidence = best_prediction["score"]

        # Convert 10-class prediction to our 2 categories
        classification = CATEGORY_MAP.get(
            detected_type,
            "unknown"
        )

        return {
            "classification": classification,
            "detected_type": detected_type,
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

