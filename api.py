from fastapi import FastAPI
import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0")
app = FastAPI()

def run_cmd(cmd, capture=False):
    print(f"📌 Esecuzione: {cmd[:100]}")
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"   → {result.stdout[:200] if result.stdout else '(nessun output)'}")
        if result.stderr:
            print(f"   ⚠️ Stderr: {result.stderr[:200]}")
        return result
    else:
        subprocess.run(cmd, shell=True)

@app.get("/test/login")
def test_login():
    print("="*50)
    print("🔐 TEST LOGIN - Controllo passo passo")
    print("="*50)
    
    # 1. Chiudi sessioni precedenti
    print("\n1️⃣ CHIUSURA SESSIONI")
    run_cmd("browser-use close --all")
    time.sleep(1)
    
    # 2. Login al cloud
    print("\n2️⃣ LOGIN AL CLOUD")
    run_cmd(f"browser-use cloud login {API_KEY}")
    time.sleep(1)
    
    # 3. Connetti browser cloud
    print("\n3️⃣ CONNESSIONE BROWSER CLOUD")
    run_cmd("browser-use cloud connect")
    time.sleep(2)
    
    # 4. Apri la pagina
    print("\n4️⃣ APRI PAGINA")
    run_cmd("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(4)
    
    # 5. VERIFICA che la pagina sia caricata
    print("\n5️⃣ VERIFICA PAGINA")
    result = run_cmd("browser-use eval 'document.title'", capture=True)
    print(f"   📄 Titolo pagina: {result.stdout.strip()}")
    
    # 6. Inserisci email
    print("\n6️⃣ INSERIMENTO EMAIL")
    run_cmd('browser-use keys "Tab"')
    time.sleep(0.5)
    run_cmd('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    
    # 7. Inserisci password
    print("\n7️⃣ INSERIMENTO PASSWORD")
    run_cmd('browser-use keys "Tab"')
    time.sleep(0.5)
    run_cmd('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # 8. VERIFICA che i campi siano compilati
    print("\n8️⃣ VERIFICA CAMPI")
    email_value = run_cmd("browser-use eval 'document.querySelector(\"input[name=username]\").value'", capture=True)
    print(f"   📧 Email inserita: {email_value.stdout.strip()}")
    
    # 9. Click login
    print("\n9️⃣ CLICK LOGIN")
    run_cmd('browser-use keys "Enter"')
    
    # 10. Monitora redirect (10 secondi)
    print("\n🔟 MONITORAGGIO REDIRECT (10 sec)")
    for i in range(10):
        time.sleep(1)
        result = run_cmd("browser-use eval 'window.location.href'", capture=True)
        url = result.stdout.strip()
        print(f"   {i+1}s → {url[:60]}")
        if "surf" in url:
            print("   ✅ REDIRECT RIUSCITO!")
            break
    
    # 11. Prendi i cookie
    print("\n1️⃣1️⃣ ESTRAZIONE COOKIE")
    result = run_cmd("browser-use cookies get", capture=True)
    print(f"\n📋 OUTPUT COMPLETO COOKIE:\n{result.stdout[:500]}")
    
    # 12. Cerca sesids e user_id
    sesids_match = re.search(r"'sesids': '([^']+)'", result.stdout)
    user_id_match = re.search(r"'user_id': '([^']+)'", result.stdout)
    
    print("\n" + "="*50)
    print("📊 RISULTATO FINALE")
    print(f"   sesids = {sesids_match.group(1) if sesids_match else '❌ NON TROVATO'}")
    print(f"   user_id = {user_id_match.group(1) if user_id_match else '❌ NON TROVATO'}")
    print("="*50)
    
    return {
        "sesids": sesids_match.group(1) if sesids_match else None,
        "user_id": user_id_match.group(1) if user_id_match else None,
        "url_finale": url if 'url' in locals() else None
    }

@app.get("/health")
def health():
    return {"status": "ok"}
