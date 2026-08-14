# Waste Classification — Project & About Me

## About the Project

This repository contains an AI-powered Waste Classification API that uses a vision model to classify images of waste into categories (e.g., recyclable, biological, trash). The service is built with FastAPI and leverages the Hugging Face `transformers` pipeline for image classification.

## About Me

I am a final-year student and developer building practical machine learning systems that solve real-world problems. My primary focus areas are computer vision, model deployment, and backend APIs. I enjoy taking ML prototypes and turning them into reliable web services that are easy to run and integrate.

Core strengths:

- Python (production-quality code)
- FastAPI for building REST APIs
- Computer vision and model inference with Hugging Face Transformers
- Model deployment and containerization (Docker)
- Working knowledge of PyTorch and image preprocessing

## Quickstart (Local)

1. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies (from project root):

```bash
pip install -r requirements.txt
```

3. Run the API (development):

```bash
# Use the venv Python to avoid user-site packages
export PYTHONNOUSERSITE=1
python -m uvicorn waste-classification.app:app --host 0.0.0.0 --port 8000 --reload
```

4. Open `http://127.0.0.1:8000/docs` for interactive API docs (Swagger UI).

## API Endpoints

- `GET /` — Health check and service info.
- `POST /classify` — Upload an image file to receive a classification result.

Example `curl` request for `/classify`:

```bash
curl -X POST "http://127.0.0.1:8000/classify" -F "file=@/path/to/image.jpg"
```

Response example:

```json
{
  "classification": "recyclable",
  "detected_type": "Plastic",
  "confidence": 0.9234
}
```

## Notes & Troubleshooting

- This project uses Hugging Face models and may download model files on first run — ensure you have a stable internet connection and enough disk space.
- If you run into version conflicts with `transformers` / `tokenizers`, prefer running inside a clean virtual environment and pin compatible versions in `requirements.txt`.

---
# waste-classification
Waste Classification
