# Waste Classification

A local waste-sorting web app that lets a user upload or take a photo, classify it, and see the recommended disposal method.

## Tech Stack

- FastAPI backend
- React + Vite frontend
- Local-only development on your machine

## Project Structure

```bash
waste-classification/
├── app.py
├── requirements.txt
├── pytest.ini
├── tests/
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
└── README.md
```

## 1) Setup the Python environment

From the parent folder:

```bash
cd /home/meru/Desktop/FINAL_YEAR/Done/waste
python3 -m venv venv
source venv/bin/activate
```

Then in the project folder:

```bash
cd waste-classification
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2) Start the backend API

```bash
cd /home/meru/Desktop/FINAL_YEAR/Done/waste/waste-classification
source ../venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will run at:

- http://localhost:8000
- http://localhost:8000/docs

## 3) Start the frontend

Open a second terminal and run:

```bash
cd /home/meru/Desktop/FINAL_YEAR/Done/waste/waste-classification/frontend
npm install
npm run dev -- --host 0.0.0.0
```

Open the app in your browser:

- http://localhost:5173

## 4) Use the app

- Choose an image from your device or use a mobile camera
- Click “Classify Waste”
- View the detected waste type and disposal advice

## API endpoint

### POST /classify

Upload an image file:

```bash
curl -X POST "http://localhost:8000/classify" -F "file=@/path/to/waste-image.jpg"
```

Example response:

```json
{
  "classification": "recyclable",
  "detected_type": "Plastic",
  "confidence": 0.8600,
  "explanation": "Plastic is commonly recyclable. This item looks recyclable. Please rinse or clean it if needed and place it in the recycling bin."
}
```

## Notes

- This project is designed to run locally on your machine.
- The backend supports localhost CORS for the React frontend at port 5173.
- If the Hugging Face model is unavailable, the app falls back to a simple local heuristic so the app still works for demos and testing.

## Test run

```bash
cd /home/meru/Desktop/FINAL_YEAR/Done/waste/waste-classification
source ../venv/bin/activate
pytest -q
```
