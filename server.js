const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// CORS setup taaki frontend se error na aaye
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'ngrok-skip-browser-warning', 'Accept']
}));

app.use(express.json());

// API Route
app.get('/api/vehicle-details-only', async (req, res) => {
  try {
    const rawRegNo = req.query.regn_no;

    if (!rawRegNo) {
      return res.status(400).json({ error: "Registration number required hai." });
    }

    // Vehicle number clean karna
    let cleanRegNo = rawRegNo.split('(')[0].split('%')[0].trim();
    cleanRegNo = cleanRegNo.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();

    if (!cleanRegNo) {
      return res.status(400).json({ error: "Valid registration number enter karein." });
    }

    // Complete upstream URL with mobile_no parameter
    const targetUrl = `https://apex.renewbuyinsurance.com/api/v1/vaahan/registration_number/?regn_no=${cleanRegNo}&partner_code=EI00350819&mobile_no=9876543210&source=apex&originData=false`;

    const response = await fetch(targetUrl, {
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://apex.renewbuyinsurance.com/'
      }
    });

    if (!response.ok) {
      return res.status(response.status).json({
        error: `Upstream error (${response.status}). Record unavailable or rate-limited.`
      });
    }

    const data = await response.json();
    return res.json(data);

  } catch (error) {
    return res.status(500).json({ error: "Failed to fetch vehicle details." });
  }
});

app.get('/', (req, res) => {
  res.send("API Server Live Hai!");
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
