import requests
URL = "http://127.0.0.1:8000"
def test_main() -> None:
    # Respuesta esperada
    expected_response = {"Hola:": "FastApi"}
    # Respuesta del servido o api
    response = requests.get(url="http://127.0.0.1:8000/main")
    print(response) 
    print(response.content)
    print(response.json())

test_main()