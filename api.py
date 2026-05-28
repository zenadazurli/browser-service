from fastapi import FastAPI
import subprocess
import os

API_KEY = "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0"
app = FastAPI()

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"CMD: {cmd[:100]}")
    print(f"STDOUT: {result.stdout[:200]}")
    print(f"STDERR: {result.stderr[:200]}")
    return result

@app.get("/test/connect")
def test_connect():
    # Configura la API key nel CLI
    run_cmd(f"browser-use config set api_key {API_KEY}")
    
    # Ora connetti
    result = run_cmd("browser-use cloud connect")
    
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

@app.get("/test/login")
def test_login():
    # Configura la API key
    run_cmd(f"browser-use config set api_key {API_KEY}")
    run_cmd("browser-use cloud connect")
    run_cmd("browser-use open https://www.easyhits4u.com/logon/")
    run_cmd('browser-use keys "Tab"')
    run_cmd('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    run_cmd('browser-use keys "Tab"')
    run_cmd('browser-use type "DDnmVV45!!"')
    run_cmd('browser-use keys "Enter"')
    
    result = run_cmd("browser-use cookies get")
    
    import re
    sesids_match = re.search(r"'sesids': '([^']+)'", result.stdout)
    user_id_match = re.search(r"'user_id': '([^']+)'", result.stdout)
    
    return {
        "sesids": sesids_match.group(1) if sesids_match else None,
        "user_id": user_id_match.group(1) if user_id_match else None,
        "raw_output": result.stdout[:500]
    }

@app.get("/health")
def health():
    return {"status": "ok"}
