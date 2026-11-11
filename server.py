from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

@app.get("/proxy")
async def proxy_mastodon(instance: str):
    target_url = f"https://{instance}/api/v1/timelines/public?local=true&limit=5"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, headers={"User-Agent": "MastoRama-CloudProxy/1.0"})
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))