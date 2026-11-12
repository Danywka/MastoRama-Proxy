from fastapi import FastAPI, HTTPException, Response
import httpx

app = FastAPI()

@app.get("/proxy")
async def proxy(instance: str):
    clean_instance = instance.replace("https://", "").replace("http://", "").strip('/')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://{clean_instance}/api/v1/timelines/public", timeout=10.0)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/image-proxy")
async def proxy_image(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Missing URL parameter")
    
    async with httpx.AsyncClient() as client:
        try:
            # Скачиваем картинку с современного сервера с поддержкой свежего TLS
            response = await client.get(url, timeout=15.0, follow_redirects=True)
            
            content_type = response.headers.get("content-type", "image/jpeg")
            
            return Response(content=response.content, media_type=content_type)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))