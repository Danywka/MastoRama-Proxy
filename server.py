from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

BEARER_TOKEN = "BM2aMc9dG4nyy9cq_19RNR4ZOIOwq8TvCID05YldU8U"

@app.get("/proxy")
async def proxy_mastodon(instance: str):
    # Очищаем инстанс от лишнего мусора, если пользователь вписал с https://
    clean_instance = instance.replace("https://", "").replace("http://", "").strip('/')
    
    # Динамически подставляем тот сервер, который попросили (`mastodon.world`, `fosstodon.org` и т.д.)
    target_url = f"https://{clean_instance}/api/v1/timelines/public?limit=10"
    
    headers = {
        "User-Agent": "MastoRama-CloudProxy/1.0",
        "Authorization": f"Bearer {BEARER_TOKEN.strip()}"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, headers=headers)
            print(f"Proxying to {clean_instance}, status: {response.status_code}")
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Mastodon ({clean_instance}) returned {response.status_code}: {response.text}")
                
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))