import io

from fastapi.testclient import TestClient
from PIL import Image

import app as app_module

client = TestClient(app_module.app)


def test_api_root_is_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_classify_returns_explanation(monkeypatch):
    def fake_classifier(image):
        return [{"label": "Plastic", "score": 0.96}]

    monkeypatch.setattr(app_module, "classifier", fake_classifier)

    image = Image.new("RGB", (128, 128), color="blue")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    response = client.post(
        "/classify",
        files={"file": ("waste.jpg", buffer.read(), "image/jpeg")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["classification"] == "recyclable"
    assert payload["detected_type"] == "Plastic"
    assert "explanation" in payload
    assert "plastic" in payload["explanation"].lower()
