import requests

URL = "http://127.0.0.1:8000"

def test_create_user():
    request ={
        "name": "Jhon",
        "lastname": "Doe",
        "age":21, 
        "email": "correo",
        "password": "Hola Mundo",
        "cv": "nombre_cv.pdf"
    }
    expected_response = {
        "user_id": 1,
        "name": "Jhon",
        "lastname": "Doe",
        "age":21, 
        "email": "correo"
    }
    response = requests.post(url=f"{URL}/users", json=request)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == expected_response
test_create_user()
