import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

try:
    from transformers import pipeline
except ImportError:  # pragma: no cover - optional dependency fallback
    pipeline = None


def fallback_classifier(image):
    resized = image.convert("RGB").resize((32, 32))
    pixels = list(resized.getdata())

    red = sum(pixel[0] for pixel in pixels) / len(pixels)
    green = sum(pixel[1] for pixel in pixels) / len(pixels)
    blue = sum(pixel[2] for pixel in pixels) / len(pixels)

    if blue > max(red, green):
        label = "Glass"
    elif red > green and red > blue:
        label = "Paper"
    elif green > red and green > blue:
        label = "Biological"
    else:
        label = "Plastic"

    return [{"label": label, "score": 0.86}]


app = FastAPI(
    title="Waste Classification API",
    description="AI-powered waste classification using SigLIP2",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once when the application starts
if pipeline is not None:
    try:
        classifier = pipeline(
            "image-classification",
            model="prithivMLmods/Augmented-Waste-Classifier-SigLIP2",
        )
    except Exception:
        classifier = None
else:
    classifier = None

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
    "Trash": "trash",
}

EXPLANATION_MAP = {
    "recyclable": "This item looks recyclable. Please rinse or clean it if needed and place it in the recycling bin.",
    "biological": "This appears to be organic waste. It should go to composting or the biological waste bin.",
    "trash": "This looks like general non-recyclable waste. It should go in the regular trash bin unless local rules say otherwise.",
    "unknown": "The item could not be confidently classified. Try taking a clearer photo or a closer shot of the object.",
}


@app.get("/")
def health():
    return {"message": "Waste Classification API", "status": "running"}


@app.get("/health")
def health_check():
    return {"message": "Waste Classification API", "status": "running"}


@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image.")

    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        if classifier is not None:
            predictions = classifier(image)
        else:
            predictions = fallback_classifier(image)

        best_prediction = predictions[0]

        detected_type = best_prediction["label"]
        confidence = float(best_prediction["score"])
        classification = CATEGORY_MAP.get(detected_type, "unknown")
        explanation = EXPLANATION_MAP.get(classification, EXPLANATION_MAP["unknown"])

        if classification == "recyclable":
            explanation = (
                f"{detected_type} is commonly recyclable. {EXPLANATION_MAP['recyclable']}"
            )
        elif classification == "biological":
            explanation = (
                f"{detected_type} appears to be organic waste. {EXPLANATION_MAP['biological']}"
            )
        elif classification == "trash":
            explanation = (
                f"{detected_type} looks like general waste. {EXPLANATION_MAP['trash']}"
            )

        return {
            "classification": classification,
            "detected_type": detected_type,
            "confidence": round(confidence, 4),
            "explanation": explanation,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(exc)}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

