from fastapi import FastAPI
import asyncio
import logging
import sys
import os
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

app = FastAPI()

PROXY = {
    "server": "http://resi.fusionproxy.net:13822",
    "username": "sazz16014w96",
    "password": "t3vz152mql23"
}

async def get_cookies_async():
    logger.info("🚀 Avvio Playwright...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        # Crea contesto con proxy
        context = await browser.new_context(proxy=PROXY)
        page = await context.new_page()
        
        logger.info("🌐 Navigazione...")
        await page.goto("https://www.easyhits4u.com/logon/", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # Chiudi overlay
        await page.evaluate("""
            document.querySelectorAll('.ReactModal__Overlay, .modal-overlay').forEach(el => {
                el.style.display = 'none';
            });
        """)
        
        logger.info("📝 Compilazione form...")
        await page.fill('input[name="username"]', "sandrominori50+ulugarecexisa@gmail.com")
        await page.fill('input[name="password"]', "DDnmVV45!!")
        
        logger.info("🔑 Click login...")
        await page.click('button.btn_green', force=True)
        
        logger.info("⏳ Attesa redirect...")
        for i in range(30):
            await page.wait_for_timeout(1000)
            if "surf" in page.url:
                logger.info(f"✅ Redirect rilevato! URL: {page.url}")
                break
        
        logger.info("🍪 Estrazione cookie...")
        cookies = await context.cookies()
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
