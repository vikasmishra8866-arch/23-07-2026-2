from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()


# 1. Yeh route aapka sundar web page browser me kholega
@app.get("/", response_class=HTMLResponse)
def home_page():
  return """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <title>Vehicle Details Finder</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f7f6; padding: 30px; }
            .box { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            input, button { width: 100%; padding: 10px; margin-top: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
            button { background: #007bff; color: white; font-weight: bold; cursor: pointer; }
            button:hover { background: #0056b3; }
            pre { background: #212529; color: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 15px; overflow-x: auto; display: none; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Vehicle Service Portal</h2>
            <label>Token daalein:</label>
            <input type="text" id="token" placeholder="Apna in-auth-token yahan paste karein">
            
            <label>Gaadi ka Number:</label>
            <input type="text" id="number" placeholder="Jaise: GJ05HG7801">
            
            <button onclick="getData()">Details Nikalein</button>
            <pre id="result"></pre>
        </div>

        <script>
            async function getData() {
                const token = document.getElementById('token').value;
                const number = document.getElementById('number').value;
                const resultBox = document.getElementById('result');
                
                if(!token || !number) {
                    alert("Token aur Number dono bharein!");
                    return;
                }

                resultBox.style.display = "block";
                resultBox.innerText = "Data fetch ho raha hai...";

                try {
                    const response = await window.fetch(`/call-tata-aig?number=${number}&token=${token}`);
                    const data = await response.json();
                    resultBox.innerText = JSON.stringify(data, null, 4);
                } catch(e) {
                    resultBox.innerText = "Error aa gayi: " + e;
                }
            }
        </script>
    </body>
    </html>
    """


# 2. Yeh wahi aapka original working API function hai
@app.get("/call-tata-aig")
def call_external_api(number: str, token: str):
  target_url = (
      "https://sellmotor.tataaig.com/api/v1/motornstpservice/getVahanInfo"
  )

  custom_headers = {
      "Origin": "https://sellonline.tataaig.com",
      "Referer": "https://sellonline.tataaig.com/",
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      ),
      "in-auth-token": token.strip(),
      "Content-Type": "application/json",
  }

  payload = {
      "rcnumber": number.strip().upper(),
      "vehicle_type": "TW",
      "calling_system": "IPDS-V2",
  }

  try:
    api_response = requests.post(
        target_url, headers=custom_headers, json=payload, timeout=10
    )
    api_data = api_response.json()
  except Exception as e:
    api_data = {"error": "API call fail ho gayi", "details": str(e)}

  return {
      "status": "success",
      "vehicle_no": number.strip().upper(),
      "tataaig_response": api_data,
  }
