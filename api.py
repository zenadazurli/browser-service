from fastapi import FastAPI
import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0")

app = FastAPI()  # <--- FONDAMENTALE: senza questa, l'app non parte

def run_cmd(cmd, capture_output=False):
    print(f"📌 Esecuzione: {cmd[:80]}...")
    if capture_output:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"   → {result.stdout[:100] if result.stdout else '(nessun output)'}")
        return result
    else:
        subprocess.run(cmd, shell=True)

@app.get("/test/login")
def test_login():
    print("="*50)
    print("🔐 TEST LOGIN")
    print("="*50)

    run_cmd(f"browser-use config set api_key {API_KEY}")
    run_cmd("browser-use cloud connect")
    time.sleep(2)
    run_cmd("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(5)
    run_cmd('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run_cmd('browser-use keys "Tab"')
    time.sleep(1)
    run_cmd('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    run_cmd('browser-use keys "Enter"')
    time.sleep(8)
    result = run_cmd("browser-use cookies get", capture_output=True)

    sesids_match = re.search(r"'sesids': '([^']+)'", result.stdout)
    user_id_match = re.search(r"'user_id': '([^']+)'", result.stdout)

    print(f"   sesids = {sesids_match.group(1) if sesids_match else '❌ NON TROVATO'}")
    print(f"   user_id = {user_id_match.group(1) if user_id_match else '❌ NON TROVATO'}")

    return {
        "sesids": sesids_match.group(1) if sesids_match else None,
        "user_id": user_id_match.group(1) if user_id_match else None
    }

@app.get("/health")
def health():
    return {"status": "ok"}
