from fastapi import FastAPI

app = FastAPI()

@app.get("/app")
async def main() -> dict:
    return {"Hola": "Mundo"}