from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/proxy")
async def proxy(instance: str):
    clean_instance = instance.replace("https://", "").replace("http://", "").strip('/')
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://{clean_instance}/api/v1/timelines/public")
        return response.json()