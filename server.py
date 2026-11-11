from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

BEARER_TOKEN = "BM2aMc9dG4nyy9cq_19RNR4ZOIOwq8TvCID05YldU8U"

@app.get("/proxy")
async def proxy_mastodon(instance: str):
    # Запрашиваем общую публичную ленту
    target_url = f"https://{instance}/api/v1/timelines/public?limit=5"
    
    headers = {
        "User-Agent": "MastoRama-CloudProxy/1.0",
        "Authorization": f"Bearer {BEARER_TOKEN.strip()}"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, headers=headers)
            print(f"Mastodon status: {response.status_code}, response: {response.text}")
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Mastodon returned {response.status_code}: {response.text}")
                
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))