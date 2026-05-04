# VaidyaAI — AYUSH Intelligence Platform

AI-powered healthcare platform for India's 12,000+ AYUSH centres. Built on Indian AI models, deployed on GCP asia-south1.

## Modules

- **Voice EHR Engine** — Multilingual voice-to-EHR using IndicConformer ASR. Reduces patient record creation from 8 minutes to under 30 seconds.
- **Treatment Recommender** — 3-layer engine combining CCRAS protocol rules, patient similarity matching, and Airavata LLM for Prakriti-aware treatment plans.
- **Outbreak Surveillance** — ARIMA + Isolation Forest anomaly detection across districts. Flags disease spikes within 24 hours.
- **Feedback Loop** — Clinician accept/modify/reject feedback continuously retrains recommendations.

## Tech Stack

- **Backend** — FastAPI, Python 3.10, GCP asia-south1
- **ASR** — IndicConformer 600M (ai4bharat)
- **NER** — IndicBERT
- **Translation** — IndicTrans2
- **LLM** — Airavata-7B (self-hosted)
- **Surveillance** — ARIMA, Isolation Forest, DBSCAN
- **Web Server** — Nginx (reverse proxy)

## Setup

### Requirements

```bash
pip install fastapi uvicorn torch torchaudio transformers
```

### Environment Variables

```bash
export HF_TOKEN=your_huggingface_token
```

### Start Mock Server (Demo)

```bash
nohup uvicorn mock_server:app --host 127.0.0.1 --port 8001 > /tmp/vaidyaai_server.log 2>&1 &
```

### Start Real Backend

```bash
nohup uvicorn ayush_app:app --host 127.0.0.1 --port 8001 > /tmp/vaidyaai_server.log 2>&1 &
```

### Nginx

```bash
sudo cp nginx_vaidyaai.conf /etc/nginx/sites-available/vaidyaai
sudo ln -sf /etc/nginx/sites-available/vaidyaai /etc/nginx/sites-enabled/vaidyaai
sudo nginx -t && sudo systemctl reload nginx
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Frontend |
| `/api/ehr/create` | POST | Voice → EHR |
| `/api/ehr/{ehr_id}` | GET | Fetch EHR |
| `/api/recommend/treatment` | POST | Generate treatment plan |
| `/api/recommend/feedback` | POST | Submit clinician feedback |
| `/api/surveillance/alerts` | GET | Active outbreak alerts |
| `/health` | GET | Health check |

## URLs

| | URL |
|---|---|
| Frontend | http://34.93.151.212/ |
| Health Check | http://34.93.151.212/health |
| API Docs | http://34.93.151.212:8001/docs |

## Switching Mock → Real Backend

```bash
# Demo mode
./start_mock.sh

# Real AI mode (after ayush_app.py is ready)
./start_real.sh
```

## Built By

YellowSense Technologies Pvt. Ltd.  
DPIIT Recognised · TIDE 2.0 · Incubated at IIIT Bangalore Innovation Centre  
Submission: IndiaAI Mission — Ministry of AYUSH PS3
