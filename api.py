@app.get("/test/screenshot")
def take_screenshot():
    # Configura API key
    subprocess.run(f"browser-use config set api_key {API_KEY}", shell=True)
    
    # Connetti e apri la pagina
    subprocess.run("browser-use cloud connect", shell=True)
    time.sleep(2)
    subprocess.run("browser-use open https://www.easyhits4u.com/logon/", shell=True)
    time.sleep(5)
    
    # Inserisci dati
    subprocess.run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"', shell=True)
    time.sleep(1)
    subprocess.run('browser-use keys "Tab"', shell=True)
    time.sleep(1)
    subprocess.run('browser-use type "DDnmVV45!!"', shell=True)
    time.sleep(1)
    
    # Fai screenshot PRIMA di premere Enter
    subprocess.run("browser-use screenshot before_login.png", shell=True)
    
    # Premi Enter
    subprocess.run('browser-use keys "Enter"', shell=True)
    time.sleep(5)
    
    # Fai screenshot DOPO Enter
    subprocess.run("browser-use screenshot after_login.png", shell=True)
    
    return {"message": "Screenshot salvati: before_login.png, after_login.png"}
