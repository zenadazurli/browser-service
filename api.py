@app.get("/test/save_screenshots")
def save_screenshots():
    import os
    
    # Crea directory per gli screenshot
    os.makedirs("/tmp/screenshots", exist_ok=True)
    
    # Configura API key
    subprocess.run(f"browser-use config set api_key {API_KEY}", shell=True)
    
    # Connetti e apri la pagina
    subprocess.run("browser-use cloud connect", shell=True)
    time.sleep(2)
    subprocess.run("browser-use open https://www.easyhits4u.com/logon/", shell=True)
    time.sleep(5)
    subprocess.run("browser-use screenshot /tmp/screenshots/1_before.png", shell=True)
    
    # Compila e invia
    subprocess.run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"', shell=True)
    time.sleep(1)
    subprocess.run('browser-use keys "Tab"', shell=True)
    time.sleep(1)
    subprocess.run('browser-use type "DDnmVV45!!"', shell=True)
    time.sleep(1)
    subprocess.run("browser-use screenshot /tmp/screenshots/2_filled.png", shell=True)
    
    subprocess.run('browser-use keys "Enter"', shell=True)
    time.sleep(8)
    subprocess.run("browser-use screenshot /tmp/screenshots/3_after_login.png", shell=True)
    
    return {"message": "Screenshot salvati in /tmp/screenshots/"}
