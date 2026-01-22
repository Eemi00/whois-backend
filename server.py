from fastapi import FastAPI
from api import get_whois_data
from fastapi.middleware.cors import CORSMiddleware

# Määritetään app FastAPIn kautta
app = FastAPI()

# Merkataan sivuston ROOT tällä koodille
@app.get("/")
def read_root():
    return {"status": "API is online", "docs": "/docs"}

# Testataan haku tällä
@app.get("/search")
def search(domain: str):
    return get_whois_data(domain)