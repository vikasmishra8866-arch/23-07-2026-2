from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# CORS allow karna zaroori hai taaki HTML page local ya live server se baat kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestData(BaseModel):
    token: str
    vehicle_number: str


@app.post("/get-vehicle-details")
def get_vehicle_details(data: RequestData):
    target_url = "https://sellmotor.tataaig.com/api/v1/motornstpservice/getVahanInfo"

    custom_headers = {
        "Origin": "https://sellonline.tataaig.com",
        "Referer": "https://sellonline.tataaig.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "in-auth-token": data.token.strip(),
        "Content-Type": "application/json",
    }

    payload = {
        "rcnumber": data.vehicle_number.strip().upper(),
        "vehicle_type": "TW",
        "calling_system": "IPDS-V2",
    }

    try:
        api_response = requests.post(
            target_url, headers=custom_headers, json=payload, timeout=10
        )
        return api_response.json()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"API call fail ho gayi: {str(e)}"
        )
