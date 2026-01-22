from fastapi import FastAPI
from api import get_whois_data

# Määritetään app FastAPIn kautta
app = FastAPI()

# Merkataan sivuston ROOT tällä koodille
@app.get("/")
def home():
    return {"message": "Domain API is running"}

# Testataan haku tällä
@app.get("/search")
def search(domain: str):
    message = get_whois_data(domain)
    return {"status": message}