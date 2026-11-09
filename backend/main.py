import base64
import json
import os
import re
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

from farming_service import get_farming_advice, get_structured_farming_advice
from platform_service import (
    GOVERNMENT_SCHEMES,
    KNOWLEDGE_GUIDES,
    add_community_comment,
    add_timeline_activity,
    analyze_crop_issue,
    calculate_irrigation_plan,
    check_scheme_eligibility,
    compare_market_decision,
    create_community_post,
    delete_zone,
    explain_farm_zone,
    get_all_zones,
    get_community_posts,
    get_crop_doctor_history,
    get_daily_action_plan,
    get_market_prices,
    get_nearby_resources,
    get_timeline_activities,
    get_weather_intelligence,
    like_community_post,
    register_or_login_farmer,
    simulate_what_if,
    toggle_timeline_status,
    upsert_zone,
)

load_dotenv()

app = FastAPI(
    title="AgriVoice AI — Smart Agriculture Platform API",
    description="Next-Generation Multilingual Agricultural Voice Assistant, Digital Twin Farm Map, Crop Doctor, Weather Intelligence & Farmer Ecosystem.",
    version="2.0.0",
)

raw_origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
allowed_origins = list(
    {origin.strip() for origin in raw_origins if origin.strip()}
    | {"http://localhost:5173", "http://127.0.0.1:5173"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GNANI_API_KEY = os.getenv("GNANI_API_KEY", "").strip()
PRISMA_URL = "https://api.vachana.ai/stt/v3"
TIMBRE_URL = "https://api.vachana.ai/api/v1/tts/sse"

LANGUAGES = {
    "te-IN": {"name": "Telugu", "native": "తెలుగు", "stt_supported": True, "tts_supported": True},
    "hi-IN": {"name": "Hindi", "native": "हिन्दी", "stt_supported": True, "tts_supported": True},
    "ta-IN": {"name": "Tamil", "native": "தமிழ்", "stt_supported": True, "tts_supported": True},
    "kn-IN": {"name": "Kannada", "native": "ಕನ್ನಡ", "stt_supported": True, "tts_supported": True},
    "ml-IN": {"name": "Malayalam", "native": "മലയാളം", "stt_supported": True, "tts_supported": True},
    "en-IN": {"name": "English", "native": "English", "stt_supported": True, "tts_supported": True},
}


class AdviceRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    language_code: str = "en-IN"
    category: Optional[str] = None


class SpeakRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1500)
    language_code: str = "en-IN"


def require_api_key():
    if not GNANI_API_KEY or GNANI_API_KEY == "PASTE_YOUR_GNANI_API_KEY_HERE":
        raise HTTPException(
            status_code=503,
            detail="Gnani API key is not configured on the server. Add GNANI_API_KEY in backend/.env and restart the backend.",
        )


@app.get("/")
def home():
    return {
        "message": "AgriVoice AI Smart Agriculture Platform backend is running",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
def health():
    configured = bool(GNANI_API_KEY and GNANI_API_KEY != "PASTE_YOUR_GNANI_API_KEY_HERE")
    vision_configured = bool(os.getenv("VISION_API_KEY", "").strip())
    return {
        "status": "ok",
        "gnani_key_configured": configured,
        "vision_key_configured": vision_configured,
        "services": {
            "stt": "Gnani Prisma V3.0",
            "tts": "Gnani Timbre",
            "guidance": "AgriVoice Structured Agricultural Knowledge Engine",
            "weather": "Open-Meteo Live Meteorological Integration",
            "database": "SQLite Persistent Farm & Community Store",
        },
        "supported_languages": list(LANGUAGES.keys()),
    }


@app.get("/api/languages")
def list_languages():
    return {
        "languages": [
            {"code": code, **info} for code, info in LANGUAGES.items()
        ]
    }


# ==============================================================================
# VOICE & AI ASSISTANT ENDPOINTS (PRESERVED + ENHANCED)
# ==============================================================================
@app.post("/api/transcribe")
async def transcribe(
    audio_file: UploadFile = File(...),
    language_code: str = Form("te-IN"),
):
    require_api_key()
    if language_code not in LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language selection.")

    audio = await audio_file.read()
    if not audio:
        raise HTTPException(
            status_code=400,
            detail="The uploaded audio recording is empty. Please speak clearly and try again.",
        )
    if len(audio) > 12 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Audio recording is too large (max 12 MB). Please record a shorter clip to conserve API credits.",
        )

    filename = audio_file.filename or "farmer-recording.wav"
    content_type = audio_file.content_type or "audio/wav"

    files = {
        "audio_file": (
            filename,
            audio,
            content_type,
        )
    }
    data = {
        "model": "prisma-v3.0",
        "language_code": language_code,
        "preferred_language": language_code,
        "format": "transcribe",
        "itn_native_numerals": "true",
    }
    headers = {"X-API-Key-ID": GNANI_API_KEY}

    try:
        result = requests.post(
            PRISMA_URL, headers=headers, data=data, files=files, timeout=90
        )
        if result.status_code in (401, 403):
            raise HTTPException(
                status_code=502,
                detail="Gnani Prisma authentication failed or account access is restricted. Please verify your Gnani API key and account entitlements.",
            )
        if result.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Gnani API rate limit or credit quota reached. Please use text input to conserve credits.",
            )
        if not result.ok:
            api_msg = ""
            try:
                err_json = result.json()
                if isinstance(err_json, dict):
                    api_msg = str(
                        err_json.get("detail")
                        or err_json.get("message")
                        or err_json.get("error")
                        or ""
                    )
            except Exception:
                api_msg = result.text[:250] if result.text else ""
            raise HTTPException(
                status_code=502,
                detail=f"Gnani Prisma returned status {result.status_code}{': ' + api_msg if api_msg else ''}.",
            )
        payload = result.json()
    except HTTPException:
        raise
    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Speech recognition request timed out. Please try a shorter voice recording.",
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to Gnani Prisma speech recognition service. Check your internet connection.",
        )
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="Speech recognition service returned an unreadable response.",
        )

    transcript = (
        payload.get("transcript")
        or payload.get("text")
        or (
            payload.get("data", {}).get("transcript")
            if isinstance(payload.get("data"), dict)
            else None
        )
    )
    if not transcript or not str(transcript).strip():
        raise HTTPException(
            status_code=422,
            detail="No clear speech was detected in the recording. Please speak closer to the microphone or type your question.",
        )
    return {
        "transcript": str(transcript).strip(),
        "language_code": language_code,
        "provider": "Gnani Prisma V3.0",
    }


@app.post("/api/advice")
def advice(request: AdviceRequest):
    question_clean = request.question.strip()
    if not question_clean:
        raise HTTPException(
            status_code=400, detail="Please enter a valid agricultural question."
        )
    if request.language_code not in LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language selection.")

    structured = get_structured_farming_advice(
        question_clean,
        request.language_code,
        request.category or "",
    )
    return {
        "answer": structured["answer"],
        "category": structured["category"],
        "sections": structured["sections"],
        "language_code": request.language_code,
        "source": "AgriVoice Agricultural Knowledge Engine",
        "notice": structured["notice"],
    }


@app.post("/api/speak")
def speak(request: SpeakRequest):
    require_api_key()
    if request.language_code not in LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language selection.")

    voice = os.getenv("TIMBRE_VOICE", "Karan")
    model = os.getenv("TIMBRE_MODEL", "vachana-voice-v3")
    clean_text = request.text.strip()[:900]

    payload = {
        "audio_config": {
            "bitrate": "192k",
            "container": "mp3",
            "encoding": "linear_pcm",
            "num_channels": 1,
            "sample_rate": 44100,
            "sample_width": 2,
        },
        "model": model,
        "text": clean_text,
        "voice": voice,
    }
    headers = {"X-API-Key-ID": GNANI_API_KEY, "Content-Type": "application/json"}

    try:
        result = requests.post(TIMBRE_URL, json=payload, headers=headers, timeout=90)
        if result.status_code in (401, 403):
            raise HTTPException(
                status_code=502,
                detail="Gnani Timbre authentication or voice entitlement failed. Check your API key and TIMBRE_MODEL / TIMBRE_VOICE settings.",
            )
        if result.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Gnani API credit quota or rate limit reached. Voice generation is paused; you can still read the text response.",
            )
        if not result.ok:
            raise HTTPException(
                status_code=502,
                detail=f"Voice generation service returned HTTP {result.status_code}. You can still read the text guidance.",
            )
    except HTTPException:
        raise
    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Voice generation timed out. You can still read the text guidance.",
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to reach Gnani Timbre voice service. Please check your internet connection.",
        )

    chunks = []
    for line in result.text.splitlines():
        if line.startswith("data:"):
            value = line[5:].strip()
            if not value or value == "[DONE]":
                continue
            try:
                event = json.loads(value)
                if isinstance(event, dict):
                    encoded = (
                        event.get("audio")
                        or event.get("audio_chunk")
                        or event.get("data")
                    )
                    if encoded:
                        chunks.append(encoded)
            except json.JSONDecodeError:
                if re.fullmatch(r"[A-Za-z0-9+/=]+", value):
                    chunks.append(value)

    if not chunks:
        try:
            direct_json = result.json()
            if isinstance(direct_json, dict):
                direct_audio = (
                    direct_json.get("audio")
                    or direct_json.get("audio_chunk")
                    or direct_json.get("data")
                )
                if isinstance(direct_audio, str) and direct_audio:
                    chunks.append(direct_audio)
        except Exception:
            pass

    if not chunks:
        raise HTTPException(
            status_code=502,
            detail="Voice generation completed without audio data. Verify TIMBRE_MODEL and TIMBRE_VOICE in backend/.env.",
        )

    try:
        audio_bytes = b"".join(base64.b64decode(chunk) for chunk in chunks)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Could not decode audio stream returned by Gnani Timbre.",
        )

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'inline; filename="agrivoice-answer.mp3"'},
    )


# ==============================================================================
# SMART FARM MAP, DIGITAL TWIN & TIMELINE ENDPOINTS
# ==============================================================================
@app.get("/api/farm/zones")
def api_get_zones(lat: float = Query(16.3067), lng: float = Query(80.4365)):
    zones = get_all_zones()
    resources = get_nearby_resources(lat, lng)
    daily_plan = get_daily_action_plan()
    return {
        "zones": zones,
        "nearby_resources": resources,
        "daily_action_plan": daily_plan,
        "data_label": "Demonstration & Farmer-Entered Digital Twin Records",
    }


@app.post("/api/farm/zones")
def api_upsert_zone(payload: Dict[str, Any]):
    zone = upsert_zone(payload)
    return {"zone": zone, "zones": get_all_zones()}


@app.delete("/api/farm/zones/{zone_id}")
def api_delete_zone(zone_id: str):
    delete_zone(zone_id)
    return {"zones": get_all_zones()}


@app.post("/api/farm/explain")
def api_explain_zone(payload: Dict[str, Any]):
    zone_id = payload.get("zone_id", "zone-a")
    return explain_farm_zone(zone_id)


@app.get("/api/farm/timeline")
def api_get_timeline():
    return {
        "timeline": get_timeline_activities(),
        "daily_action_plan": get_daily_action_plan(),
    }


@app.post("/api/farm/timeline")
def api_add_timeline(payload: Dict[str, Any]):
    item = add_timeline_activity(payload)
    return {"item": item, "timeline": get_timeline_activities()}


@app.patch("/api/farm/timeline/{item_id}")
def api_toggle_timeline(item_id: int):
    updated = toggle_timeline_status(item_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Timeline activity not found.")
    return {"item": updated, "timeline": get_timeline_activities()}


# ==============================================================================
# WEATHER INTELLIGENCE & IRRIGATION / WHAT-IF SIMULATOR
# ==============================================================================
@app.get("/api/weather")
def api_get_weather(lat: float = Query(16.3067), lng: float = Query(80.4365)):
    return get_weather_intelligence(lat, lng)


@app.post("/api/irrigation/plan")
def api_irrigation_plan(payload: Dict[str, Any]):
    return calculate_irrigation_plan(payload)


@app.post("/api/simulator/what-if")
def api_what_if(payload: Dict[str, Any]):
    return simulate_what_if(payload)


# ==============================================================================
# AI CROP DOCTOR
# ==============================================================================
@app.post("/api/crop-doctor/analyze")
async def api_crop_doctor_analyze(
    crop_name: str = Form("Tomato"),
    symptom_notes: str = Form(""),
    image_file: Optional[UploadFile] = File(None),
):
    filename = "field-observation.jpg"
    file_size = 0
    if image_file:
        content = await image_file.read()
        file_size = len(content)
        filename = image_file.filename or "crop-photo.jpg"
        if file_size > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Uploaded image exceeds 10 MB limit. Please choose a smaller photograph.",
            )

    analysis = analyze_crop_issue(crop_name, symptom_notes, filename, file_size)
    return {
        "analysis": analysis,
        "history": get_crop_doctor_history(),
    }


@app.get("/api/crop-doctor/history")
def api_crop_doctor_history():
    return {"history": get_crop_doctor_history()}


# ==============================================================================
# MARKET INSIGHTS, GUIDES, SCHEMES, COMMUNITY & PROFILE
# ==============================================================================
@app.get("/api/market/prices")
def api_market_prices(crop: str = Query(""), state: str = Query("")):
    return get_market_prices(crop, state)


@app.post("/api/market/assistant")
def api_market_assistant(payload: Dict[str, Any]):
    crop_name = payload.get("crop", "Paddy")
    return compare_market_decision(crop_name)


@app.get("/api/guides")
def api_guides(category: str = Query(""), search: str = Query("")):
    items = KNOWLEDGE_GUIDES
    if category and category != "All":
        items = [g for g in items if g["category"].lower() == category.lower()]
    if search:
        s = search.lower()
        items = [
            g
            for g in items
            if s in g["title"].lower()
            or s in g["crops"].lower()
            or s in g["summary"].lower()
        ]
    return {"guides": items}


@app.get("/api/schemes")
def api_schemes(category: str = Query("")):
    items = GOVERNMENT_SCHEMES
    if category and category != "All":
        items = [
            s
            for s in items
            if s["category"].lower() == category.lower()
            or s["level"].lower() == category.lower()
        ]
    return {"schemes": items}


@app.post("/api/schemes/eligibility")
def api_schemes_eligibility(payload: Dict[str, Any]):
    return check_scheme_eligibility(payload)


@app.get("/api/community/posts")
def api_get_posts(category: str = Query("")):
    return {"posts": get_community_posts(category)}


@app.post("/api/community/posts")
def api_create_post(payload: Dict[str, Any]):
    if not (payload.get("title") or "").strip() or not (payload.get("content") or "").strip():
        raise HTTPException(
            status_code=400, detail="Please enter both a title and description for your post."
        )
    post = create_community_post(payload)
    return {"post": post, "posts": get_community_posts()}


@app.post("/api/community/posts/{post_id}/like")
def api_like_post(post_id: int):
    updated = like_community_post(post_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Community post not found.")
    return {"post": updated, "posts": get_community_posts()}


@app.post("/api/community/posts/{post_id}/comment")
def api_comment_post(post_id: int, payload: Dict[str, Any]):
    text = (payload.get("text") or "").strip()
    author = (payload.get("author") or "Farmer").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter a comment.")
    updated = add_community_comment(post_id, author, text)
    if not updated:
        raise HTTPException(status_code=404, detail="Community post not found.")
    return {"post": updated, "posts": get_community_posts()}


@app.post("/api/auth/profile")
def api_auth_profile(payload: Dict[str, Any]):
    user = register_or_login_farmer(payload)
    return {"user": user}
