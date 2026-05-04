"""
VaidyaAI Mock Server
====================
Runs on port 8001. Returns realistic hardcoded responses for all endpoints.
Frontend cannot tell the difference between this and the real ayush_app.py.

Usage:
    pip install fastapi uvicorn
    uvicorn mock_server:app --host 0.0.0.0 --port 8001 --reload

When real backend is ready:
    Just stop this server and start ayush_app.py on port 8001.
    Frontend needs ZERO changes.
"""

import asyncio
import random
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI(title="VaidyaAI Mock Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request schemas (must match ayush_app.py exactly) ────────────────────────

class EHRRequest(BaseModel):
    audioBase64: str
    languageCode: str = "hi"
    doctorId: str = "DOC001"
    centerId: str = "CTR001"
    districtId: str = "DIST001"

class RecommendRequest(BaseModel):
    ehr_id: str

class FeedbackRequest(BaseModel):
    plan_id: str
    action: str
    modifications: Optional[Dict] = {}
    reason_tag: Optional[str] = None

# ── Realistic mock data pools ─────────────────────────────────────────────────

TRANSCRIPTS = {
    "hi": "मरीज का नाम राहुल शर्मा है, उम्र 45 साल, पुरुष। रक्तचाप बढ़ा हुआ है, सिरदर्द और थकान की शिकायत है। प्रकृति पित्त-कफ है।",
    "kn": "ರೋಗಿಯ ಹೆಸರು ರಮೇಶ್ ಕುಮಾರ್, ವಯಸ್ಸು 52 ವರ್ಷ, ಪುರುಷ. ರಕ್ತದೊತ್ತಡ ಹೆಚ್ಚಾಗಿದೆ, ತಲೆನೋವು ಮತ್ತು ಆಯಾಸ.",
    "ta": "நோயாளியின் பெயர் சுரேஷ் குமார், வயது 38, ஆண். சிறுநீரக கல் பிரச்சனை, வாதம் பிரகிருதி.",
    "te": "రోగి పేరు వెంకట్ రావు, వయసు 60 సంవత్సరాలు, పురుషుడు. అధిక బీపీ, తలనొప్పి.",
    "en": "Patient name is Rahul Sharma, age 45, male. Complaints of high blood pressure, headache and fatigue. Prakriti is Pitta-Kapha.",
}

MOCK_EHRS = {
    "EHR001": {
        "ehr_id": "EHR001",
        "transcript": TRANSCRIPTS["hi"],
        "entities": {
            "patient_name": "Rahul Sharma",
            "age": 45,
            "gender": "Male",
            "prakriti": "Pitta-Kapha",
            "symptoms": ["headache", "fatigue", "dizziness"],
            "diagnosis_raw": "Hypertension",
            "namc_code": "AY-HYP-01",
            "icd10_code": "I10",
            "comorbidities": [],
        },
        "timestamp": "2026-02-27T10:30:00",
    },
    "EHR002": {
        "ehr_id": "EHR002",
        "transcript": TRANSCRIPTS["ta"],
        "entities": {
            "patient_name": "Suresh Kumar",
            "age": 38,
            "gender": "Male",
            "prakriti": "Vata",
            "symptoms": ["pain", "burning"],
            "diagnosis_raw": "Nephrolithiasis",
            "namc_code": "AY-NEP-01",
            "icd10_code": "N20",
            "comorbidities": [],
        },
        "timestamp": "2026-02-27T11:15:00",
    },
}

MOCK_PLANS = {
    "PLN001": {
        "plan_id": "PLN001",
        "ehr_id": "EHR001",
        "herbal": [
            {"item": "Brahmi (Bacopa monnieri) — 500mg twice daily", "type": "herbal", "confidence": 0.89, "evidence": "CCRAS Protocol AY-HYP-07: Pitta-dominant hypertension. 3 similar patients improved significantly at 4-week follow-up."},
            {"item": "Arjuna (Terminalia arjuna) — 500mg twice daily", "type": "herbal", "confidence": 0.85, "evidence": "Classical cardiotonic herb, AYUSH Ministry guidelines for Stage 1 hypertension in Pitta-Kapha constitution."},
            {"item": "Sarpagandha — as per physician discretion", "type": "herbal", "confidence": 0.76, "evidence": "Evidence from 12 similar Pitta-Kapha patients at Dharwad AYUSH centre, 2024-25."},
        ],
        "dietary": [
            {"item": "Avoid spicy, oily, and salty foods", "type": "dietary", "confidence": 0.93, "evidence": "Pitta-pacifying dietary guidelines — Charaka Samhita Sutrasthana Ch. 26."},
            {"item": "Coconut water daily (200ml morning)", "type": "dietary", "confidence": 0.88, "evidence": "Cooling and diuretic effect; recommended in Pitta-Kapha hypertension by CCRAS."},
            {"item": "Increase bitter greens: bitter gourd, neem leaves", "type": "dietary", "confidence": 0.81, "evidence": "Kapha-reducing dietary protocol, AYUSH Ministry guidelines."},
        ],
        "yoga": [
            {"item": "Sheetali Pranayama — 10 minutes, morning", "type": "yoga", "confidence": 0.87, "evidence": "Cooling breath technique for Pitta constitution. Proven BP reduction effect in 3-month trial."},
            {"item": "Shavasana — 20 minutes daily", "type": "yoga", "confidence": 0.91, "evidence": "Stress-reduction standard for hypertension; highest acceptance rate in doctor feedback."},
            {"item": "Chandra Bhedana — 5 minutes, night", "type": "yoga", "confidence": 0.79, "evidence": "Left-nostril breathing activates parasympathetic system; recommended for Pitta types."},
        ],
        "narrative": "For Rahul Sharma, a 45-year-old male with Pitta-Kapha Prakriti and Stage 1 hypertension, we recommend a cooling therapeutic approach. Brahmi and Arjuna will support cardiovascular health and mental calm, while Sarpagandha can be considered under physician supervision. Dietary modifications focusing on Pitta-pacifying foods — especially reducing spicy and salty intake — are essential. Sheetali Pranayama and Shavasana daily will help manage stress-related blood pressure elevation. Follow up in 14 days to assess response.",
        "followup_days": 14,
        "timestamp": "2026-02-27T10:31:00",
    }
}

MOCK_ALERTS = [
    {
        "alert_id": "ALT001",
        "disease": "Nephrolithiasis",
        "namc_code": "AY-NEP-01",
        "district": "Dharwad, Karnataka",
        "cases_last_7d": 47,
        "baseline_expected": 12.0,
        "deviation_factor": 3.9,
        "severity": "CRITICAL",
        "cluster_radius_km": 8.2,
        "recommended_action": "Deploy mobile AYUSH camp immediately. Alert District Health Officer. Initiate mass screening for Nephrolithiasis.",
        "timestamp": datetime.utcnow().isoformat(),
        "lat": 15.46,
        "lng": 75.01,
    },
    {
        "alert_id": "ALT002",
        "disease": "Hypertension",
        "namc_code": "AY-HYP-01",
        "district": "Ahmedabad, Gujarat",
        "cases_last_7d": 58,
        "baseline_expected": 18.0,
        "deviation_factor": 3.2,
        "severity": "HIGH",
        "cluster_radius_km": 14.5,
        "recommended_action": "Deploy AYUSH team within 48 hours. Increase Brahmi and Arjuna stock at PHCs in cluster.",
        "timestamp": datetime.utcnow().isoformat(),
        "lat": 23.02,
        "lng": 72.57,
    },
    {
        "alert_id": "ALT003",
        "disease": "Obesity",
        "namc_code": "AY-OBE-01",
        "district": "Mysuru, Karnataka",
        "cases_last_7d": 31,
        "baseline_expected": 14.0,
        "deviation_factor": 2.2,
        "severity": "MEDIUM",
        "cluster_radius_km": 20.1,
        "recommended_action": "Monitor Obesity cases daily. Alert block-level AYUSH officers in Mysuru.",
        "timestamp": datetime.utcnow().isoformat(),
        "lat": 12.29,
        "lng": 76.64,
    },
]

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post("/api/ehr/create")
async def create_ehr(req: EHRRequest):
    """Simulates 2-3 second ASR processing delay, then returns realistic EHR."""
    await asyncio.sleep(2.5)  # simulate real ASR latency
    lang = req.languageCode.split("-")[0].lower()
    transcript = TRANSCRIPTS.get(lang, TRANSCRIPTS["hi"])
    ehr_id = random.choice(list(MOCK_EHRS.keys()))
    ehr = MOCK_EHRS[ehr_id].copy()
    ehr["transcript"] = transcript
    ehr["timestamp"] = datetime.utcnow().isoformat()
    return ehr


@app.get("/api/ehr/{ehr_id}")
async def get_ehr(ehr_id: str):
    return MOCK_EHRS.get(ehr_id, MOCK_EHRS["EHR001"])


@app.post("/api/recommend/treatment")
async def get_treatment(req: RecommendRequest):
    """Simulates 1-2 second LLM generation delay."""
    await asyncio.sleep(1.5)
    plan = MOCK_PLANS["PLN001"].copy()
    plan["ehr_id"] = req.ehr_id
    plan["timestamp"] = datetime.utcnow().isoformat()
    return plan


@app.post("/api/recommend/feedback")
async def submit_feedback(req: FeedbackRequest):
    await asyncio.sleep(0.3)
    return {"status": "ok", "feedback_id": f"FB{random.randint(1000,9999)}"}


@app.get("/api/recommend/feedback/summary")
async def feedback_summary():
    return {"total": 24, "accepted": 17, "modified": 5, "rejected": 2, "acceptance_rate": 70.8}


@app.get("/api/surveillance/alerts")
async def get_alerts():
    await asyncio.sleep(0.5)
    return {
        "alerts": MOCK_ALERTS,
        "districts_monitored": 10,
        "last_run": datetime.utcnow().isoformat(),
    }


@app.get("/api/surveillance/map-data")
async def get_map_data():
    features = []
    district_coords = {
        "Dharwad, Karnataka":  (15.46, 75.01),
        "Ahmedabad, Gujarat":  (23.02, 72.57),
        "Mysuru, Karnataka":   (12.29, 76.64),
        "Belagavi, Karnataka": (15.85, 74.50),
        "Pune, Maharashtra":   (18.52, 73.86),
        "Jaipur, Rajasthan":   (26.91, 75.79),
        "Surat, Gujarat":      (21.17, 72.83),
        "Nagpur, Maharashtra": (21.14, 79.08),
    }
    alert_map = {a["district"]: a for a in MOCK_ALERTS}
    for name, (lat, lng) in district_coords.items():
        alert = alert_map.get(name)
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "district": name,
                "has_alert": alert is not None,
                "severity": alert["severity"] if alert else "NORMAL",
                "disease": alert["disease"] if alert else None,
                "cases_7d": alert["cases_last_7d"] if alert else 0,
                "deviation": alert["deviation_factor"] if alert else 1.0,
            }
        })
    return {"type": "FeatureCollection", "features": features}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "mode": "MOCK — swap to ayush_app.py for real inference",
        "service": "VaidyaAI",
        "data_residency": "GCP asia-south1 (Mumbai, India)",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mock_server:app", host="0.0.0.0", port=8001, reload=True)
