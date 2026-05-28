from fastapi import FastAPI
import subprocess
import time
import re
import os
import threading

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0")
app = FastAPI()

# Variabile globale per la sessione
session_active = False
session_lock = threading.Lock()

def run_cmd(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def init_session():
    global session_active
    with session_lock:
        if not session_active:
            print("🚀 Inizializzazione sessione cloud persistente...")
            run_cmd("browser-use close --all")
            run_cmd(f"browser-use cloud login {API_KEY}")
            run_cmd("browser-use cloud connect")
            run_cmd("browser-use open https://www.easyhits4u.com/logon/")
            session_active = True
            print("✅ Sessione cloud pronta")

@app.get("/cookies")
def get_cookies():
    print("🔐 Ottenimento cookie...")
    
    # Assicura che la sessione sia attiva
    init_session()
    
    # Chiudi eventuali modali
    run_cmd('browser-use keys "Escape"')
    time.sleep(1)
    
    # Naviga alla pagina di login (se non ci sei già)
    run_cmd("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(2)
    
    # Pulisci eventuali campi precompilati
    run_cmd('browser-use keys "Tab"')
    run_cmd('browser-use keys "Ctrl+A"')
    run_cmd('browser-use type ""')
    time.sleep(0.5)
    
    # Compila form
    run_cmd('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(0.5)
    
    run_cmd('browser-use keys "Tab"')
    run_cmd('browser-use type "DDnmVV45!!"')
    time.sleep(0.5)
    
    # Login
    run_cmd('browser-use keys "Enter"')
    time.sleep(5)
    
    # Verifica redirect
    result = run_cmd("browser-use eval 'window.location.href'", capture=True)
    
    # Se siamo su warning, riprova
    tentativi = 1
    while "warning" in result.stdout and tentativi < 3:
        print(f"⚠️ Tentativo {tentativi} fallito, riprovo...")
        run_cmd('browser-use keys "Enter"')
        time.sleep(5)
        result = run_cmd("browser-use eval 'window.location.href'", capture=True)
        tentativi += 1
    
    # Aspetta redirect
    for i in range(20):
        time.sleep(1)
        result = run_cmd("browser-use eval 'window.location.href'", capture=True)
        if "/surf/" in result.stdout:
            print("✅ Redirect rilevato!")
            break
    
    # Estrai cookie
    result = run_cmd("browser-use cookies get", capture=True)
    
    sesids_match = re.search(r"'sesids': '([^']+)'", result.stdout)
    user_id_match = re.search(r"'user_id': '([^']+)'", result.stdout)
    
    sesids = sesids_match.group(1) if sesids_match else None
    user_id = user_id_match.group(1) if user_id_match else None
    
    print(f"✅ Cookie: sesids={sesids}, user_id={user_id}")
    
    # NON chiudere la sessione! La lasciamo attiva.
    
    return {"sesids": sesids, "user_id": user_id}

@app.get("/health")
def health():
    return {"status": "ok"}
