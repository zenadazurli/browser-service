from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

@app.get("/test/connect")
def test_connect():
    os.environ["BROWSER_USE_API_KEY"] = "bu_MN6wlSbFKdRNKvxB349PKTYLjrHGjXGEt3DHrT91cD0"
    
    result = subprocess.run("browser-use cloud connect", shell=True, capture_output=True, text=True)
    
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

@app.get("/health")
def health():
    return {"status": "ok"}
