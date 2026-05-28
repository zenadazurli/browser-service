from fastapi import FastAPI
import subprocess
import time
import re
import os
import base64

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0")
app = FastAPI()

def run_cmd(cmd, capture_output=False):
    print(f"📌 {cmd[:80]}")
    if capture_output:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result
    else:
        subprocess.run(cmd, shell=True)

def take_screenshot_base64():
    result = run_cmd("browser-use screenshot -", capture_output=True)
    if result and result.stdout:
        return base64.b64encode(result.stdout.encode()).decode()
    return None

@app.get("/test/login")
def test_login():
    print("="*50)
    print("🔐 TEST LOGIN CON SCREENSHOT")
    print("="*50)

    # 1. Configura API key
    run_cmd(f"browser-use config set api_key {API_KEY}")
    
    # 2. Connetti cloud
    run_cmd("browser-use cloud connect")
    time.sleep(2)
    
    # 3. Apri pagina
    run_cmd("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(5)
    
    # SCREENSHOT 1: dopo apertura pagina
    img1 = take_screenshot_base64()
    
    # 4. Inserisci email
    run_cmd('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    
    # 5. Password
    run_cmd('browser-use keys "Tab"')
    time.sleep(1)
    run_cmd('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # SCREENSHOT 2: dopo compilazione
    img2 = take_screenshot_base64()
    
    # 6. Login
    run_cmd('browser-use keys "Enter"')
    time.sleep(8)
    
    # SCREENSHOT 3: dopo login
    img3 = take_screenshot_base64()
    
    # 7. Cookie
    result = run_cmd("browser-use cookies get", capture_output=True)
    
    # 8. Parsing
    sesids_match = re.search(r"'sesids': '([^']+)'", result.stdout if result else "")
    user_id_match = re.search(r"'user_id': '([^']+)'", result.stdout if result else "")
    
    return {
        "sesids": sesids_match.group(1) if sesids_match else None,
        "user_id": user_id_match.group(1) if user_id_match else None,
        "screenshots": {
            "after_open": img1[:100] + "..." if img1 else None,
            "after_fill": img2[:100] + "..." if img2 else None,
            "after_login": img3[:100] + "..." if img3 else None
        }
    }

@app.get("/health")
def health():
    return {"status": "ok"}
