from fastapi import FastAPI
import asyncio
import logging
import sys
import os
from browser_use import Browser

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

app = FastAPI()

# Imposta la API key
os.environ["BROWSER_USE_API_KEY"] = "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0"

async def get_cookies_async():
    logger.info("🚀 Avvio Browser Use SDK...")
    
    # Browser in modalità cloud
    browser = Browser(
        use_cloud=True,
        headless=True,
        proxy_country_code="it"
    )
    
    page = await browser.get_page()
    
    logger.info("🌐 Navigazione...")
    await page.goto("https://www.easyhits4u.com/logon/", wait_until="domcontentloaded")
    await page.wait_for_timeout(3000)
    
    logger.info("📝 Compilazione form...")
    await page.fill('input[name="username"]', "sandrominori50+ulugarecexisa@gmail.com")
    await page.fill('input[name="password"]', "DDnmVV45!!")
    
    logger.info("🔑 Click login...")
    await page.click('button.btn_green', force=True)
    
    logger.info("⏳ Attesa redirect...")
    await page.wait_for_url(lambda url: "surf" in url, timeout=30000)
    
    logger.info("🍪 Estrazione cookie...")
    cookies = await page.context.cookies()
    await browser.close()
    
    sesids = next((c['value'] for c in cookies if c['name'] == 'sesids'), None)
    user_id = next((c['value'] for c in cookies if c['name'] == 'user_id'), None)
    
    logger.info(f"🎉 Cookie: sesids={sesids}, user_id={user_id}")
    return {"sesids": sesids, "user_id": user_id}

@app.get("/cookies")
async def get_cookies():
    try:
        return await get_cookies_async()
    except Exception as e:
        logger.error(f"❌ Errore: {e}")
        return {"sesids": None, "user_id": None, "error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok"}
