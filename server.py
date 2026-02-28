from fastapi import FastAPI
from api import get_whois_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"status": "API is online"}

@app.get("/search")
def search(domain: str):
    try:
        return get_whois_data(domain)
    except Exception as e:
        # Don't crash the API. Return a predictable JSON error.
        return {"error": str(e)}