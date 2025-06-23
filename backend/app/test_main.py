from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "msg" in response.json()

def test_create_and_get_ci():
    ci = {
        "nombre": "TestCI",
        "tipo": "Hardware",
        "descripcion": "CI para pruebas",
        "ambiente": "DEV",
        "estado_actual": "Activo"
    }
    # Completa con campos mínimos requeridos
    response = client.post("/cis/", json=ci)
    assert response.status_code == 200
    data = response.json()
    ci_id = data["id"]
    
    response = client.get(f"/cis/{ci_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "TestCI"

def test_busqueda_ci():
    response = client.get("/cis/search/?texto=Test")
    assert response.status_code == 200
   
