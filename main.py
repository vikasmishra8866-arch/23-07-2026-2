from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/call-tata-aig")
def call_external_api(number: str, token: str):
    target_url = "https://sellmotor.tataaig.com/api/v1/motornstpservice/getVahanInfo"

    custom_headers = {
        "Origin": "https://sellonline.tataaig.com",
        "Referer": "https://sellonline.tataaig.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "in-auth-token": token.strip(),
        "Content-Type": "application/json",
    }

    payload = {
        "rcnumber": number.strip().upper(),
        "vehicle_type": "TW",
        "calling_system": "IPDS-V2"
    }

    try:
        api_response = requests.post(target_url, headers=custom_headers, json=payload, timeout=10)
        api_data = api_response.json()
    except Exception as e:
        api_data = {"error": "API call fail ho gayi", "details": str(e)}

    return {
        "status": "success",
        "vehicle_no": number.strip().upper(),
        "tataaig_response": api_data,
    }
