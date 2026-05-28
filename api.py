from fastapi import FastAPI
import subprocess
import time
import re
import os
import threading

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0")
app = FastAPI()

# Sessione globale (inizializzata una sola volta)
session_initialized = False
session_lock = threading.Lock()

def run_cmd(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def init_session():
    global session_initialized
    with session_lock:
        if not session_initialized:
            print("🚀 Inizializzazione sessione cloud (una volta sola)...")
            run_cmd("browser-use close --all")
            run_cmd(f"browser-use cloud login {API_KEY}")
            run_cmd("browser-use cloud connect")
            run_cmd("browser-use open https://www.easyhits4u.com/logon/")
            session_initialized = True
            print("✅ Sessione cloud pronta e persistente")

@app.get("/cookies")
def get_cookies():
    print("🔐 Richiesta cookie...")
    
    # Inizializza la sessione (solo la prima volta)
    init_session()
    
    # Ricompila il form (la sessione è già aperta)
    run_cmd('browser-use keys "Tab"')
    run_cmd('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(0.5)
    
    run_cmd('browser-use keys "Tab"')
    run_cmd('browser-use type "DDnmVV45!!"')
    time.sleep(0.5)
    
    # Tentativi di login
    for tentativo in range(1, 4):
        run_cmd('browser-use keys "Enter"')
        time.sleep(5)
        
        result = run_cmd("browser-use eval 'window.location.href'", capture=True)
        if "/surf/" in result.stdout:
            print(f"✅ Login OK al tentativo {tentativo}")
            break
    
    # Cookie
    result = run_cmd("browser-use cookies get", capture=True)
    
    sesids_match = re.search(r"'sesids': '([^']+)'", result.stdout)
    user_id_match = re.search(r"'user_id': '([^']+)'", result.stdout)
    
    sesids = sesids_match.group(1) if sesids_match else None
    user_id = user_id_match.group(1) if user_id_match else None
    
    print(f"🍪 Cookie: sesids={sesids}, user_id={user_id}")
    
    return {"sesids": sesids, "user_id": user_id}

@app.get("/health")
def health():
    return {"status": "ok"}
