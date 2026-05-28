from fastapi import FastAPI
from browser_use import Agent, Browser
from browser_use.llm import ChatBrowserUse  # <--- LLM INTEGRATO
import asyncio
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Chiavi (impostate come variabili d'ambiente su Render)
os.environ["BROWSER_USE_API_KEY"] = "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0"

async def get_cookies_async():
    logger.info("🚀 Avvio agente Browser Use Cloud...")
    
    # Browser in modalità cloud
    browser = Browser(
        use_cloud=True,
        proxy_country_code="it"
    )
    
    # LLM INTEGRATO di Browser Use (non richiede OpenAI)
    llm = ChatBrowserUse()
    
    agent = Agent(
        task="""
        1. Vai su https://www.easyhits4u.com/logon/
        2. Aspetta che la pagina sia caricata
        3. Inserisci l'email: sandrominori50+ulugarecexisa@gmail.com
        4. Inserisci la password: DDnmVV45!!
        5. Clicca sul pulsante di login
        6. Aspetta che l'URL diventi https://www.easyhits4u.com/surf/
        7. Estrai i cookie 'sesids' e 'user_id' dalla pagina
        8. Restituiscili in formato JSON
        """,
        llm=llm,
        browser=browser,
    )
    
    result = await agent.run()
    
    final_result = result.final_result() if hasattr(result, 'final_result') else str(result)
    logger.info(f"Risultato agente: {final_result}")
    
    try:
        if isinstance(final_result, str):
            data = json.loads(final_result)
        else:
            data = final_result
    except:
        data = {"raw_result": final_result}
    
    await browser.close()
    return data

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
