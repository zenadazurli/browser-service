from fastapi import FastAPI
import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0")
app = FastAPI()

def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

def run_cmd_capture(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

@app.get("/cookies")
def get_cookies():
    print("🔐 Login su EasyHits4U via Browser Use Cloud...")
    
    # Connessione al cloud
    run_cmd(f"browser-use cloud login {API_KEY}")
    run_cmd("browser-use cloud connect")
    
    # Navigazione e login
    run_cmd("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(3)
    
    run_cmd('browser-use keys "Tab"')
    run_cmd('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    
    run_cmd('browser-use keys "Tab"')
    run_cmd('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    run_cmd('browser-use keys "Enter"')
    time.sleep(8)
    
    # Estrazione cookie
    result = run_cmd_capture("browser-use cookies get")
    
    sesids_match = re.search(r"'sesids': '([^']+)'", result.stdout)
    user_id_match = re.search(r"'user_id': '([^']+)'", result.stdout)
    
    sesids = sesids_match.group(1) if sesids_match else None
    user_id = user_id_match.group(1) if user_id_match else None
    
    print(f"✅ Cookie: sesids={sesids}, user_id={user_id}")
    return {"sesids": sesids, "user_id": user_id}

@app.get("/health")
def health():
    return {"status": "ok"}