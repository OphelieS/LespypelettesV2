
import django
import base64
import pytest
from django.test import RequestFactory
from django.urls import reverse
from reading.views import detect_emotion


django.setup()

@pytest.mark.django_db
def test_detect_emotion():
    # Charger une image en mémoire et la convertir en base64.
    with open("pypelette/photo_test.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Créer une requête POST avec l'image encodée en base64.
    factory = RequestFactory()
    request = factory.post(reverse("detect_emotion"), {"image": "data:image/jpeg;base64," + encoded_image})

    # Appeler la fonction `detect_emotion` avec la requête.
    response = detect_emotion(request)

    # Vérifier que la réponse est un JsonResponse et contient les clés attendues.
    assert response.status_code == 200
    assert "emotion" in response.json()