from fastapi import FastAPI
from api import get_whois_data
from fastapi.middleware.cors import CORSMiddleware

# Määritetään app FastAPIn kautta
app = FastAPI()

# Sallitaan Reactin ottaa yhteys APIin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Merkataan sivuston ROOT tällä koodille
@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"status": "API is online"}

# Testataan haku tällä
@app.get("/search")
def search(domain: str):
    return get_whois_data(domain)