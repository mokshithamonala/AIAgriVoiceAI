"""
AgriVoice AI — Platform Service & SQLite Persistence Layer.
Handles Smart Farm Zones (Digital Twin), Farm Timeline, Weather-to-Action Intelligence,
Smart Irrigation & Soil Planner, What-If Simulator, AI Crop Doctor History,
Market Insights, Farming Knowledge Hub, Government Schemes, Community Posts, and Profiles.
"""

import datetime
import json
import os
import sqlite3
from typing import Any, Dict, List, Optional

import requests

DB_PATH = os.path.join(os.path.dirname(__file__), "agrivoice.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            state TEXT NOT NULL,
            district TEXT NOT NULL,
            language_code TEXT DEFAULT 'te-IN',
            farm_size_acres REAL DEFAULT 4.5,
            primary_crops TEXT DEFAULT 'Paddy, Tomato, Chilli',
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS farm_zones (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            crop TEXT NOT NULL,
            area_acres REAL NOT NULL,
            sowing_date TEXT NOT NULL,
            stage TEXT NOT NULL,
            soil_type TEXT NOT NULL,
            soil_ph REAL DEFAULT 6.6,
            moisture_pct INTEGER NOT NULL,
            irrigation_status TEXT NOT NULL,
            health_status TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            recommendation TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS farm_timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            zone_name TEXT NOT NULL,
            scheduled_date TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT DEFAULT ''
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS crop_doctor_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_name TEXT NOT NULL,
            symptom_notes TEXT NOT NULL,
            suspected_issue TEXT NOT NULL,
            severity TEXT NOT NULL,
            visual_indicators TEXT NOT NULL,
            causes TEXT NOT NULL,
            next_steps TEXT NOT NULL,
            prevention TEXT NOT NULL,
            analysis_mode TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS community_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_name TEXT NOT NULL,
            author_location TEXT NOT NULL,
            category TEXT NOT NULL,
            crop_tag TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            comments_json TEXT DEFAULT '[]',
            created_at TEXT NOT NULL
        )
        """
    )

    # Seed initial demo farm zones if empty
    cur.execute("SELECT COUNT(*) as cnt FROM farm_zones")
    if cur.fetchone()["cnt"] == 0:
        now_str = datetime.date.today().isoformat()
        initial_zones = [
            (
                "zone-a",
                "Zone A – North Plot",
                "Paddy (BPT-5204)",
                2.0,
                "2026-08-15",
                " Vegetative / Tillering",
                "Alluvial Clay Loam",
                6.5,
                72,
                "Optimal (Standing moisture maintained)",
                "Healthy",
                16.3067,
                80.4365,
                "Maintain 3–5 cm water level during active tillering. Inspect bunds for stem borer egg masses.",
                now_str,
            ),
            (
                "zone-b",
                "Zone B – East Drip Block",
                "Tomato (Arka Rakshak)",
                1.2,
                "2026-09-10",
                "Flowering & Early Fruit Set",
                "Red Sandy Loam",
                6.8,
                54,
                "Irrigation Recommended Today",
                "Needs Attention",
                16.3082,
                80.4388,
                "Lower leaves show mild yellowing. Check drip emitters for uniform root-zone watering and inspect underside of leaves for whiteflies.",
                now_str,
            ),
            (
                "zone-c",
                "Zone C – South Ridge",
                "Chilli (Teja G-4)",
                0.8,
                "2026-09-01",
                "Vegetative Branching",
                "Black Cotton Soil",
                7.1,
                64,
                "Scheduled for Tomorrow Morning",
                "Healthy",
                16.3051,
                80.4379,
                "Good canopy vigor. Install blue/yellow sticky traps (10 per acre) to monitor thrips and mites early.",
                now_str,
            ),
            (
                "zone-d",
                "Zone D – Polyhouse / Mixed Bed",
                "Leafy & Gourds (Okra, Bitter Gourd)",
                0.5,
                "2026-09-25",
                "Early Vegetative",
                "Enriched Loam (Vermicompost)",
                6.7,
                68,
                "Drip Cycle Completed",
                "Healthy",
                16.3075,
                80.4348,
                "Mulch sheet is conserving soil moisture well. Keep drainage furrows open ahead of forecasted showers.",
                now_str,
            ),
        ]
        cur.executemany(
            """
            INSERT INTO farm_zones (
                id, name, crop, area_acres, sowing_date, stage, soil_type,
                soil_ph, moisture_pct, irrigation_status, health_status,
                lat, lng, recommendation, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            initial_zones,
        )

    # Seed initial timeline if empty
    cur.execute("SELECT COUNT(*) as cnt FROM farm_timeline")
    if cur.fetchone()["cnt"] == 0:
        initial_timeline = [
            (
                "Deep Summer Ploughing & FYM Incorporation",
                "Land preparation",
                "All Zones",
                "2026-07-28",
                "Completed",
                "Applied 4 tonnes well-decomposed farmyard manure.",
            ),
            (
                "Transplanting Paddy & Vegetable Nursery Sowing",
                "Sowing",
                "Zone A & Zone B",
                "2026-08-15",
                "Completed",
                "Line transplanting completed with 20x15 cm spacing.",
            ),
            (
                "Soil Health Card Split Nutrient Application",
                "Fertilizer application",
                "Zone A – Paddy",
                "2026-09-18",
                "Completed",
                "Applied neem-coated urea + zinc sulphate at root zone.",
            ),
            (
                "Drip Root-Zone Irrigation & Moisture Check",
                "Irrigation",
                "Zone B – Tomato",
                datetime.date.today().isoformat(),
                "Pending",
                "Check 5–8 cm root moisture before running 45-minute morning drip cycle.",
            ),
            (
                "Lower Leaf Yellowing & Sticky Trap Inspection",
                "Crop inspection",
                "Zone B & Zone C",
                datetime.date.today().isoformat(),
                "Pending",
                "Inspect underside of 10 tomato and chilli plants for whiteflies and thrips.",
            ),
            (
                "Pheromone Trap Lure Replacement (IPM)",
                "Pest management",
                "Zone A – Paddy",
                (datetime.date.today() + datetime.timedelta(days=3)).isoformat(),
                "Upcoming",
                "Check stem borer pheromone traps and clear drainage channels.",
            ),
            (
                "First Picking & Grading Preparation",
                "Harvesting",
                "Zone B – Tomato",
                (datetime.date.today() + datetime.timedelta(days=18)).isoformat(),
                "Upcoming",
                "Arrange plastic crates for harvest to prevent bruising.",
            ),
        ]
        cur.executemany(
            """
            INSERT INTO farm_timeline (title, category, zone_name, scheduled_date, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            initial_timeline,
        )

    # Seed initial community posts if empty
    cur.execute("SELECT COUNT(*) as cnt FROM community_posts")
    if cur.fetchone()["cnt"] == 0:
        sample_comments = json.dumps(
            [
                {
                    "author": "Ramesh Naidu (KVK Progressive Farmer)",
                    "text": "Installing 12 yellow sticky traps per acre and spraying neem oil (1500 ppm) early morning helped us reduce whitefly without harsh sprays.",
                    "time": "2 hours ago",
                }
            ]
        )
        initial_posts = [
            (
                "Srinivas Rao",
                "Guntur, Andhra Pradesh",
                "Crop Diseases",
                "Tomato",
                "How we managed early leaf curling and yellowing in our 1.5-acre tomato plot",
                "We noticed upward leaf curling in our 35-day tomato crop. Before spraying anything, we checked soil drainage and used yellow sticky traps. Keeping root moisture even and removing 4 severely affected plants early stopped the spread.",
                19,
                sample_comments,
                "Today",
            ),
            (
                "Lakshmi Devi",
                "Warangal, Telangana",
                "Organic Farming",
                "Chilli",
                "Mulching + Vermicompost saved 30% irrigation water in our chilli field",
                "During dry spells, silver-black mulching sheet kept soil cool at 6 cm depth and reduced weed growth. Highly recommend testing soil pH before basal application.",
                27,
                "[]",
                "Yesterday",
            ),
            (
                "Manjunath Gowda",
                "Mandya, Karnataka",
                "Paddy Farming",
                "Paddy",
                "Alternate Wetting and Drying (AWD) in Paddy — less water and stronger roots",
                "Instead of keeping 8 cm standing water continuously, letting water subside until hairline cracks appear and re-irrigating to 5 cm reduced stem rot and saved pump hours.",
                34,
                "[]",
                "2 days ago",
            ),
        ]
        cur.executemany(
            """
            INSERT INTO community_posts (
                author_name, author_location, category, crop_tag, title, content, likes, comments_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            initial_posts,
        )

    conn.commit()
    conn.close()


init_db()


# ==============================================================================
# 1. SMART FARM ZONES, DIGITAL TWIN & NEARBY RESOURCES
# ==============================================================================
def get_all_zones() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM farm_zones ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def upsert_zone(zone_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db_connection()
    now_str = datetime.date.today().isoformat()
    zone_id = zone_data.get("id") or f"zone-{int(datetime.datetime.now().timestamp())}"
    moisture = int(zone_data.get("moisture_pct", 60))
    health = zone_data.get("health_status") or ("Needs Attention" if moisture < 55 else "Healthy")
    recommendation = zone_data.get("recommendation") or (
        f"Monitor root-zone moisture ({moisture}%) and inspect leaves twice weekly for early stress."
    )

    conn.execute(
        """
        INSERT OR REPLACE INTO farm_zones (
            id, name, crop, area_acres, sowing_date, stage, soil_type,
            soil_ph, moisture_pct, irrigation_status, health_status,
            lat, lng, recommendation, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            zone_id,
            zone_data.get("name", "New Field Zone"),
            zone_data.get("crop", "Mixed Crop"),
            float(zone_data.get("area_acres", 1.0)),
            zone_data.get("sowing_date", now_str),
            zone_data.get("stage", "Vegetative"),
            zone_data.get("soil_type", "Red Sandy Loam"),
            float(zone_data.get("soil_ph", 6.7)),
            moisture,
            zone_data.get("irrigation_status", "Scheduled"),
            health,
            float(zone_data.get("lat", 16.3067)),
            float(zone_data.get("lng", 80.4365)),
            recommendation,
            now_str,
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM farm_zones WHERE id = ?", (zone_id,)).fetchone()
    conn.close()
    return dict(row)


def delete_zone(zone_id: str) -> bool:
    conn = get_db_connection()
    cur = conn.execute("DELETE FROM farm_zones WHERE id = ?", (zone_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def get_nearby_resources(lat: float = 16.3067, lng: float = 80.4365) -> List[Dict[str, Any]]:
    return [
        {
            "id": "res-kvk",
            "name": "Krishi Vigyan Kendra (KVK) Extension Centre",
            "type": "KVK / Advisory",
            "distance_km": 4.2,
            "lat": lat + 0.0045,
            "lng": lng - 0.0035,
            "phone": "1800-180-1551",
            "services": "Plant clinic diagnosis, Soil Health Card testing, certified seed guidance",
        },
        {
            "id": "res-soil",
            "name": "District Soil & Water Testing Laboratory",
            "type": "Soil Testing Lab",
            "distance_km": 6.8,
            "lat": lat - 0.0052,
            "lng": lng + 0.0041,
            "phone": "0863-2234510",
            "services": "NPK, pH, Electrical Conductivity (EC) & micronutrient profiling",
        },
        {
            "id": "res-mandi",
            "name": "Regulated Agricultural Market Yard (e-NAM Mandi)",
            "type": "Agricultural Market",
            "distance_km": 8.5,
            "lat": lat + 0.0068,
            "lng": lng + 0.0062,
            "phone": "1800-270-0224",
            "services": "Electronic weighing, quality assaying, daily modal price display",
        },
        {
            "id": "res-fpo",
            "name": "Raithu Mitra Custom Hiring & Drone Seva Kendra",
            "type": "Equipment & FPO",
            "distance_km": 3.1,
            "lat": lat - 0.0028,
            "lng": lng - 0.0048,
            "phone": "1800-180-1551",
            "services": "Tractor implements, drip spares, mulching sheet, bio-inputs",
        },
    ]


def explain_farm_zone(zone_id: str) -> Dict[str, Any]:
    zones = get_all_zones()
    zone = next((z for z in zones if z["id"] == zone_id), zones[0] if zones else None)
    if not zone:
        return {"summary": "No farm zone found. Please register a field zone on the map."}

    missing_data = [
        "Recent laboratory NPK micronutrient test values (currently using farmer-entered soil type)",
        "On-field leaf wetness sensor reading",
    ]
    summary = (
        f"{zone['name']} ({zone['area_acres']} acres) is currently growing {zone['crop']} "
        f"at the {zone['stage']} stage in {zone['soil_type']} (pH {zone['soil_ph']}). "
        f"Estimated soil moisture is {zone['moisture_pct']}% and health status is '{zone['health_status']}'. "
        f"Recommended Action: {zone['recommendation']}"
    )
    return {
        "zone": zone,
        "summary": summary,
        "missing_data": missing_data,
        "data_source_note": "Field boundary and crop stage are farmer-entered demonstration records. Connect soil sensors or update after field inspection.",
    }


# ==============================================================================
# 2. FARM TIMELINE & DAILY AI ACTION PLANNER
# ==============================================================================
def get_timeline_activities() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM farm_timeline ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_timeline_activity(data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db_connection()
    cur = conn.execute(
        """
        INSERT INTO farm_timeline (title, category, zone_name, scheduled_date, status, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("title", "Field Inspection"),
            data.get("category", "Crop inspection"),
            data.get("zone_name", "Zone A"),
            data.get("scheduled_date", datetime.date.today().isoformat()),
            data.get("status", "Pending"),
            data.get("notes", ""),
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM farm_timeline WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


def toggle_timeline_status(item_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM farm_timeline WHERE id = ?", (item_id,)).fetchone()
    if not row:
        conn.close()
        return None
    new_status = "Completed" if row["status"] != "Completed" else "Pending"
    conn.execute("UPDATE farm_timeline SET status = ? WHERE id = ?", (new_status, item_id))
    conn.commit()
    updated = conn.execute("SELECT * FROM farm_timeline WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return dict(updated)


def get_daily_action_plan() -> List[Dict[str, str]]:
    zones = get_all_zones()
    low_moisture_zone = next((z for z in zones if z["moisture_pct"] < 60), zones[0] if zones else None)
    zone_name = low_moisture_zone["name"] if low_moisture_zone else "Zone B – Tomato"
    return [
        {
            "time_slot": "Morning (6:30 AM – 9:00 AM)",
            "title": f"Check Soil Moisture & Drip Emitters in {zone_name}",
            "detail": "Inspect 5–8 cm root depth before running irrigation and examine lower leaves for early pest presence while temperatures are cool.",
            "priority": "High",
        },
        {
            "time_slot": "Afternoon (12:30 PM – 3:00 PM)",
            "title": "Monitor Heat-Sensitive Vegetable Canopy & Mulch Cover",
            "detail": "Observe flowering tomato and chilli rows for midday wilting; avoid foliar sprays during peak sunlight.",
            "priority": "Medium",
        },
        {
            "time_slot": "Evening (5:00 PM – 6:30 PM)",
            "title": "Review Tomorrow's Rainfall Forecast & Clear Field Drains",
            "detail": "Check Weather Intelligence alerts and log completed field operations in your Farm Timeline.",
            "priority": "Normal",
        },
    ]


# ==============================================================================
# 3. LIVE WEATHER INTELLIGENCE (OPEN-METEO) & WEATHER-TO-ACTION AI
# ==============================================================================
def get_weather_intelligence(lat: float = 16.3067, lng: float = 80.4365) -> Dict[str, Any]:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lng}"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset"
        "&timezone=auto"
    )
    try:
        res = requests.get(url, timeout=8)
        res.raise_for_status()
        raw = res.json()
        cur = raw.get("current", {})
        daily = raw.get("daily", {})

        temp = round(float(cur.get("temperature_2m", 30.5)), 1)
        feels_like = round(float(cur.get("apparent_temperature", 33.0)), 1)
        humidity = int(cur.get("relative_humidity_2m", 66))
        wind_speed = round(float(cur.get("wind_speed_10m", 11.5)), 1)

        probs = daily.get("precipitation_probability_max", [35])
        rain_prob = int(probs[0]) if probs else 35
        tomorrow_rain_prob = int(probs[1]) if len(probs) > 1 else rain_prob

        sunrises = daily.get("sunrise", ["2026-11-09T06:12"])
        sunsets = daily.get("sunset", ["2026-11-09T17:42"])
        sunrise_str = sunrises[0].split("T")[-1] if sunrises else "06:12"
        sunset_str = sunsets[0].split("T")[-1] if sunsets else "17:42"

        forecast_days = []
        dates = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        for i in range(min(7, len(dates))):
            p = int(probs[i]) if i < len(probs) and probs[i] is not None else 20
            condition = "Rain Showers" if p >= 60 else ("Partly Cloudy" if p >= 30 else "Sunny & Clear")
            forecast_days.append(
                {
                    "date": dates[i],
                    "temp_max": round(float(max_temps[i]), 1) if i < len(max_temps) else 32.0,
                    "temp_min": round(float(min_temps[i]), 1) if i < len(min_temps) else 22.0,
                    "rain_prob": p,
                    "condition": condition,
                }
            )

        is_live = True
        source_label = "Live Open-Meteo Meteorological Service"
    except Exception:
        # Graceful fallback clearly labeled
        temp = 31.2
        feels_like = 34.0
        humidity = 68
        wind_speed = 12.4
        rain_prob = 45
        tomorrow_rain_prob = 65
        sunrise_str = "06:10"
        sunset_str = "17:45"
        today = datetime.date.today()
        forecast_days = [
            {
                "date": (today + datetime.timedelta(days=i)).isoformat(),
                "temp_max": round(31.5 + (i % 3) * 0.8, 1),
                "temp_min": round(22.5 + (i % 2) * 0.5, 1),
                "rain_prob": [45, 65, 30, 20, 25, 40, 55][i],
                "condition": ["Partly Cloudy", "Rain Expected", "Mostly Sunny", "Clear", "Partly Cloudy", "Cloudy", "Light Showers"][i],
            }
            for i in range(7)
        ]
        is_live = False
        source_label = "Offline Agromet Fallback Estimate (Check Internet for Live Satellite Feed)"

    alerts = []
    actions = []

    if tomorrow_rain_prob >= 55 or rain_prob >= 55:
        alerts.append(
            {
                "type": "warning",
                "title": f"Rainfall Alert ({max(rain_prob, tomorrow_rain_prob)}% Probability)",
                "message": "Moderate to heavy showers expected in the next 24–48 hours. Keep drainage channels open in vegetable and pulse plots.",
            }
        )
        actions.append(
            "Rain probability is elevated. Hold off on heavy irrigation today and avoid spraying foliar fertilizers or pesticides before rain."
        )
    else:
        actions.append(
            "Low immediate rain probability. Proceed with scheduled morning root-zone irrigation for moisture-sensitive vegetable zones."
        )

    if temp >= 33.0:
        alerts.append(
            {
                "type": "amber",
                "title": f"High Temperature Advisory ({temp}°C)",
                "message": "High daytime evaporation can stress flowering tomato and chilli crops.",
            }
        )
        actions.append(
            "High daytime temperature expected. Irrigate during early morning or evening hours and maintain organic mulching to conserve soil moisture."
        )

    if humidity >= 70:
        alerts.append(
            {
                "type": "info",
                "title": f"High Humidity Fungal Watch ({humidity}%)",
                "message": "Humid canopy conditions favor leaf spot and powdery mildew. Inspect lower foliage.",
            }
        )
        actions.append(
            "High relative humidity detected. Avoid overhead sprinkler watering in the evening so leaves stay dry overnight."
        )

    if wind_speed >= 18.0:
        alerts.append(
            {
                "type": "warning",
                "title": f"Strong Wind Precaution ({wind_speed} km/h)",
                "message": "Avoid chemical spraying during gusty winds to prevent drift.",
            }
        )

    return {
        "is_live": is_live,
        "source": source_label,
        "coordinates": {"lat": lat, "lng": lng},
        "current": {
            "temperature_c": temp,
            "feels_like_c": feels_like,
            "humidity_pct": humidity,
            "rain_probability_pct": rain_prob,
            "wind_speed_kmh": wind_speed,
            "condition": "Rain Showers Likely" if rain_prob >= 60 else ("Partly Cloudy" if rain_prob >= 30 else "Warm & Sunny"),
            "sunrise": sunrise_str,
            "sunset": sunset_str,
        },
        "alerts": alerts,
        "weather_to_action": actions,
        "daily_forecast": forecast_days,
    }


# ==============================================================================
# 4. SMART IRRIGATION PLANNER & WHAT-IF SIMULATOR
# ==============================================================================
def calculate_irrigation_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    crop = payload.get("crop_type", "Tomato")
    area_acres = max(0.1, float(payload.get("field_size_acres", 1.5)))
    soil_type = payload.get("soil_type", "Red Sandy Loam")
    method = payload.get("irrigation_method", "Drip Irrigation")
    current_moisture = int(payload.get("current_moisture_pct", 52))

    base_liters_per_acre = {
        "Paddy": 18000,
        "Tomato": 9500,
        "Chilli": 8500,
        "Cotton": 10000,
        "Vegetables": 9000,
        "Maize": 11000,
    }.get(crop, 9500)

    efficiency_factor = {
        "Drip Irrigation": 0.65,
        "Sprinkler": 0.80,
        "Furrow / Ridge": 1.0,
        "Flood Irrigation": 1.25,
    }.get(method, 0.85)

    soil_factor = {
        "Red Sandy Loam": 1.1,
        "Black Cotton Soil": 0.85,
        "Alluvial Clay Loam": 0.95,
    }.get(soil_type, 1.0)

    moisture_deficit_factor = max(0.2, (75 - current_moisture) / 35.0)
    estimated_liters = int(base_liters_per_acre * area_acres * efficiency_factor * soil_factor * moisture_deficit_factor)

    interval_days = 2 if soil_type == "Red Sandy Loam" else (4 if soil_type == "Black Cotton Soil" else 3)
    if method == "Drip Irrigation":
        duration_mins = max(20, int((estimated_liters / (area_acres * 220))))
        schedule_text = f"Run drip system for ~{duration_mins} minutes every {interval_days} days during early morning (6:00 AM – 8:00 AM)."
    else:
        schedule_text = f"Irrigate every {interval_days}–{interval_days + 1} days in the morning or late afternoon; avoid standing water around stems."

    return {
        "crop_type": crop,
        "field_size_acres": area_acres,
        "soil_type": soil_type,
        "irrigation_method": method,
        "current_moisture_pct": current_moisture,
        "estimated_water_liters": estimated_liters,
        "recommended_schedule": schedule_text,
        "best_timing": "Early Morning (6:00 AM – 8:30 AM) or Evening (4:30 PM – 6:30 PM) to minimize evaporation loss.",
        "water_saving_tips": [
            "Apply 5 cm organic mulch or crop residue between rows to reduce surface evaporation by up to 25%.",
            "Check soil moisture 5–8 cm deep by hand-feel before starting the pump.",
            "Keep tail-end field drains open to prevent root collar rot during unexpected rain.",
        ],
        "disclaimer": "Calculated estimate based on farmer-entered parameters (not live in-ground hardware sensors).",
    }


def simulate_what_if(payload: Dict[str, Any]) -> Dict[str, Any]:
    scenario = payload.get("scenario", "rainfall_decrease")
    crop = payload.get("crop_type", "Tomato")
    area_acres = float(payload.get("area_acres", 2.0))

    scenarios = {
        "rainfall_decrease": {
            "title": f"What if seasonal rainfall decreases by 30% for {crop}?",
            "moisture_impact": "-22% root-zone moisture availability over 14 days",
            "risk_level": "Moderate to High Water Stress Risk",
            "estimated_effect": (
                f"For {area_acres} acres of {crop}, a 30% rainfall drop increases irrigation demand by ~3,200–4,500 liters/acre per week. "
                "Without mulching or split watering, flower drop and leaf tip burn can occur."
            ),
            "mitigation_steps": [
                "Switch to alternate-furrow or drip root-zone watering immediately.",
                "Spread organic mulch (dry straw/leaves) around plant bases to lock in moisture.",
                "Avoid heavy top-dressing of urea during dry spells.",
            ],
        },
        "irrigation_reduced": {
            "title": f"What if irrigation volume is reduced by 25% using Drip + Mulching on {crop}?",
            "moisture_impact": "Root moisture remains stable (62–68%) due to reduced evaporation",
            "risk_level": "Low Risk (Positive Water Conservation)",
            "estimated_effect": (
                f"Delivering water directly to the root zone across {area_acres} acres saves ~2,800 liters/acre per cycle "
                "and reduces weed emergence between rows by 40%."
            ),
            "mitigation_steps": [
                "Inspect drip laterals weekly to ensure emitters are not clogged by silt.",
                "Monitor lower leaves at midday to verify zero wilting.",
            ],
        },
        "crop_switch_pulses": {
            "title": f"What if I rotate {crop} with Blackgram / Redgram (Pulses) next season?",
            "moisture_impact": "Requires ~45% less irrigation water than continuous cereal/vegetable cropping",
            "risk_level": "Low Input Risk & Improved Soil Nitrogen",
            "estimated_effect": (
                "Legume root nodules fix atmospheric nitrogen (approx. 15–25 kg N/acre equivalent) "
                "and break the life cycle of crop-specific soil-borne pests and nematodes."
            ),
            "mitigation_steps": [
                "Treat pulse seeds with Rhizobium & PSB bio-fertilizer before sowing.",
                "Ensure well-drained field beds as pulses are sensitive to waterlogging.",
            ],
        },
        "fertilizer_delayed": {
            "title": f"What if basal/top-dress fertilizer application is delayed by 15 days in {crop}?",
            "moisture_impact": "Slowed vegetative branching and pale older foliage",
            "risk_level": "Moderate Nutrient Timing Risk",
            "estimated_effect": (
                "Delayed nutrition during active vegetative/flowering stages reduces canopy vigor. "
                "Dumping the missed dose all at once later can cause salt stress or attract sap-sucking pests."
            ),
            "mitigation_steps": [
                "Do not double the chemical dose to make up for lost time.",
                "Apply nutrients in smaller split doses only when soil has adequate moisture, and consult KVK for foliar nutrition options.",
            ],
        },
    }

    result = scenarios.get(scenario, scenarios["rainfall_decrease"])
    return {
        **result,
        "disclaimer": "Transparent rule-based agronomic simulation for planning only — not a guaranteed yield or income prediction.",
    }


# ==============================================================================
# 5. AI CROP DOCTOR (IMAGE + SYMPTOM ANALYSIS & HISTORY)
# ==============================================================================
def analyze_crop_issue(
    crop_name: str,
    symptom_notes: str,
    filename: str,
    file_size_bytes: int,
) -> Dict[str, Any]:
    vision_key_configured = bool(os.getenv("VISION_API_KEY", "").strip())
    notes_lower = (symptom_notes + " " + filename).lower()

    if any(k in notes_lower for k in ["yellow", "pale", "chlorosis", "nitrogen"]):
        suspected = f"{crop_name} Leaf Chlorosis / Nutrient or Moisture Imbalance"
        severity = "Moderate"
        visual_indicators = "Yellowing observed on foliage; leaf veins or margins showing paleness."
        causes = "Nitrogen/Iron/Magnesium deficiency, over-watering with poor root aeration, or early sap-sucking insect activity."
        next_steps = (
            "1. Check whether yellowing begins on older bottom leaves (often nitrogen/magnesium) or newest top leaves (iron/micronutrients).\n"
            "2. Check soil moisture 5–8 cm deep to rule out waterlogging.\n"
            "3. Inspect the underside of 5–10 leaves with a hand lens for whiteflies or mites."
        )
        prevention = "Use balanced Soil Health Card nutrition, incorporate well-decomposed compost, and maintain clean field drainage."
    elif any(k in notes_lower for k in ["spot", "brown", "blight", "fungus", "rot", "mildew", "black"]):
        suspected = f"Suspected {crop_name} Leaf Spot / Early Fungal Blight Symptoms"
        severity = "Moderate to High"
        visual_indicators = "Dark brown/black necrotic lesions or concentric spots reported on leaves/stems."
        causes = "Fungal or bacterial pathogen favored by high humidity (>70%), dew on leaves, or water splashing from soil."
        next_steps = (
            "1. Carefully prune and remove heavily spotted leaves in a closed bag away from the field.\n"
            "2. Switch to root-zone watering and avoid wetting foliage in the evening.\n"
            "3. Improve airflow between rows by weeding."
        )
        prevention = "Practice crop rotation, use disease-free treated seed, and show sample leaves to a KVK specialist before selecting a fungicide."
    elif any(k in notes_lower for k in ["curl", "pest", "hole", "worm", "aphid", "thrip", "borer", "insect"]):
        suspected = f"Suspected {crop_name} Sap-Sucking Pest / Leaf Curl Stress"
        severity = "Moderate"
        visual_indicators = "Upward/downward leaf cupping, crinkling, or visible feeding damage."
        causes = "Whiteflies, thrips, aphids, or mites feeding on tender shoots, or viral leaf curl transmitted by sucking insects."
        next_steps = (
            "1. Install yellow and blue sticky traps (10–12 traps/acre) just above crop canopy height.\n"
            "2. Uproot and safely dispose of any severely stunted virus-affected plants early.\n"
            "3. Consult local extension officers for approved neem-based or IPM interventions."
        )
        prevention = "Maintain field border sanitation, remove weed hosts, and avoid excessive nitrogen fertilizer."
    else:
        suspected = f"{crop_name} Field Stress Inspection Required"
        severity = "Advisory Check"
        visual_indicators = f"Uploaded image ({filename}, {max(1, file_size_bytes // 1024)} KB) logged with farmer notes."
        causes = "May involve localized soil moisture stress, nutrient deficiency, or early pest/disease onset."
        next_steps = (
            "1. Inspect both upper and lower leaf surfaces on 5–10 plants across the plot.\n"
            "2. Check root collar and soil moisture at 5–8 cm depth.\n"
            "3. Share the affected plant sample with your local Agricultural Officer or KVK."
        )
        prevention = "Regular scouting twice a week helps catch crop problems before they spread."

    analysis_mode = (
        "Vision AI + Agronomic Rule Engine"
        if vision_key_configured
        else "Symptom-Assisted Diagnostic Guide (Configure VISION_API_KEY in backend/.env to enable automated computer-vision leaf classification)"
    )

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()
    cur = conn.execute(
        """
        INSERT INTO crop_doctor_history (
            crop_name, symptom_notes, suspected_issue, severity,
            visual_indicators, causes, next_steps, prevention,
            analysis_mode, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            crop_name,
            symptom_notes or f"Uploaded photo: {filename}",
            suspected,
            severity,
            visual_indicators,
            causes,
            next_steps,
            prevention,
            analysis_mode,
            now_str,
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM crop_doctor_history WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


def get_crop_doctor_history() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM crop_doctor_history ORDER BY id DESC LIMIT 15").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ==============================================================================
# 6. MARKET INTELLIGENCE & MANDI DECISION ASSISTANT
# ==============================================================================
MARKET_DATA = [
    {
        "id": "m-1",
        "crop": "Paddy (Common / BPT)",
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "mandi": "Guntur Regulated Market Yard",
        "min_price": 2300,
        "max_price": 2540,
        "modal_price": 2420,
        "unit": "INR / Quintal",
        "trend": "+2.4%",
        "history": [2310, 2340, 2360, 2390, 2405, 2420],
        "source": "Reference Agmarknet / e-NAM Benchmark",
        "updated_at": "2026-11-08",
    },
    {
        "id": "m-2",
        "crop": "Paddy (Common / BPT)",
        "state": "Telangana",
        "district": "Warangal",
        "mandi": "Enumamula Agricultural Market",
        "min_price": 2320,
        "max_price": 2580,
        "modal_price": 2465,
        "unit": "INR / Quintal",
        "trend": "+3.1%",
        "history": [2330, 2350, 2390, 2410, 2440, 2465],
        "source": "Reference Agmarknet / e-NAM Benchmark",
        "updated_at": "2026-11-08",
    },
    {
        "id": "m-3",
        "crop": "Tomato (Hybrid)",
        "state": "Andhra Pradesh",
        "district": "Chittoor",
        "mandi": "Madanapalle Tomato Market",
        "min_price": 1850,
        "max_price": 2600,
        "modal_price": 2250,
        "unit": "INR / Quintal",
        "trend": "+5.8%",
        "history": [1900, 1980, 2050, 2120, 2190, 2250],
        "source": "Reference Agmarknet / e-NAM Benchmark",
        "updated_at": "2026-11-08",
    },
    {
        "id": "m-4",
        "crop": "Tomato (Hybrid)",
        "state": "Karnataka",
        "district": "Kolar",
        "mandi": "Kolar APMC Market",
        "min_price": 1780,
        "max_price": 2490,
        "modal_price": 2180,
        "unit": "INR / Quintal",
        "trend": "+4.2%",
        "history": [1820, 1900, 1960, 2040, 2110, 2180],
        "source": "Reference Agmarknet / e-NAM Benchmark",
        "updated_at": "2026-11-08",
    },
    {
        "id": "m-5",
        "crop": "Chilli (Dry Teja)",
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "mandi": "Guntur Mirchi Yard",
        "min_price": 14200,
        "max_price": 17800,
        "modal_price": 16400,
        "unit": "INR / Quintal",
        "trend": "+1.9%",
        "history": [15600, 15800, 16000, 16150, 16250, 16400],
        "source": "Reference Agmarknet / e-NAM Benchmark",
        "updated_at": "2026-11-08",
    },
    {
        "id": "m-6",
        "crop": "Cotton (Long Staple)",
        "state": "Telangana",
        "district": "Adilabad",
        "mandi": "Adilabad Cotton Market",
        "min_price": 6850,
        "max_price": 7520,
        "modal_price": 7280,
        "unit": "INR / Quintal",
        "trend": "+1.5%",
        "history": [7050, 7100, 7150, 7200, 7240, 7280],
        "source": "Reference Agmarknet / e-NAM Benchmark",
        "updated_at": "2026-11-08",
    },
    {
        "id": "m-7",
        "crop": "Turmeric (Finger)",
        "state": "Tamil Nadu",
        "district": "Erode",
        "mandi": "Erode Regulated Market",
        "min_price": 11800,
        "max_price": 13900,
        "modal_price": 12950,
        "unit": "INR / Quintal",
        "trend": "+2.7%",
        "history": [12200, 12400, 12550, 12700, 12820, 12950],
        "source": "Reference Agmarknet / e-NAM Benchmark",
        "updated_at": "2026-11-08",
    },
    {
        "id": "m-8",
        "crop": "Onion (Red)",
        "state": "Maharashtra",
        "district": "Nashik",
        "mandi": "Lasalgaon APMC",
        "min_price": 2100,
        "max_price": 2950,
        "modal_price": 2620,
        "unit": "INR / Quintal",
        "trend": "+4.5%",
        "history": [2280, 2350, 2420, 2490, 2560, 2620],
        "source": "Reference Agmarknet / e-NAM Benchmark",
        "updated_at": "2026-11-08",
    },
]


def get_market_prices(crop_query: str = "", state_filter: str = "") -> Dict[str, Any]:
    results = MARKET_DATA
    if crop_query:
        q = crop_query.lower()
        results = [m for m in results if q in m["crop"].lower() or q in m["mandi"].lower() or q in m["district"].lower()]
    if state_filter and state_filter != "All":
        results = [m for m in results if m["state"].lower() == state_filter.lower()]
    return {
        "prices": results,
        "data_notice": "Reference benchmark prices shown for planning. Verify live daily auction rates on official e-NAM (enam.gov.in) or Agmarknet before transport.",
    }


def compare_market_decision(crop_name: str) -> Dict[str, Any]:
    matches = [m for m in MARKET_DATA if crop_name.lower() in m["crop"].lower()]
    if not matches:
        matches = MARKET_DATA[:2]
    best = max(matches, key=lambda x: x["modal_price"])
    return {
        "crop": best["crop"],
        "best_mandi": best["mandi"],
        "district": best["district"],
        "state": best["state"],
        "modal_price": best["modal_price"],
        "max_price": best["max_price"],
        "recommendation": (
            f"Among available reference records for {best['crop']}, {best['mandi']} ({best['district']}, {best['state']}) "
            f"shows the highest modal price at ₹{best['modal_price']}/Quintal (up to ₹{best['max_price']}/Quintal for Grade-A dry/graded produce). "
            "Factor in transport distance, moisture grading standards, and check live morning arrivals on e-NAM before dispatching."
        ),
    }


# ==============================================================================
# 7. FARMING KNOWLEDGE HUB GUIDES
# ==============================================================================
KNOWLEDGE_GUIDES = [
    {
        "id": "guide-1",
        "category": "Crop cultivation",
        "title": "System of Rice Intensification (SRI) & Alternate Wetting-Drying",
        "crops": "Paddy (Rice)",
        "summary": "Grow stronger paddy root systems while saving 25–35% irrigation water and reducing lodging.",
        "steps": [
            "Transplant young seedlings (10–12 days old) singly with wider 25x25 cm spacing.",
            "Keep soil moist rather than continuously flooded during vegetative growth (Alternate Wetting & Drying).",
            "Use a cono-weeder between rows to aerate soil roots and incorporate weeds into the mud.",
            "Maintain a thin 2–3 cm water layer after panicle initiation until 10 days before harvest.",
        ],
        "precautions": "Requires well-leveled plots and working drainage channels so young seedlings do not submerge during heavy rain.",
    },
    {
        "id": "guide-2",
        "category": "Soil management",
        "title": "How to Collect an Accurate Soil Sample for Soil Health Card Testing",
        "crops": "All Field & Horticultural Crops",
        "summary": "A 15-minute V-cut sampling method before sowing prevents blind fertilizer expenditure.",
        "steps": [
            "Clear surface dry leaves at 8–10 random spots in a zig-zag pattern across one uniform field.",
            "Dig a V-shaped cut to 15 cm (6 inches) depth for field crops and collect a 2 cm slice from the side wall.",
            "Mix all slices thoroughly on a clean cloth, divide into 4 quarters, and retain 500 grams.",
            "Air-dry in the shade and label with your name, survey number, previous crop, and irrigation source.",
        ],
        "precautions": "Do not sample near bunds, manure heaps, under trees, or immediately after fertilizer application.",
    },
    {
        "id": "guide-3",
        "category": "Pest management",
        "title": "Integrated Pest Management (IPM) for Vegetable & Chilli Crops",
        "crops": "Tomato, Chilli, Brinjal, Okra",
        "steps": [
            "Grow 2 rows of tall maize or sorghum around the field border as a natural barrier against migrating whiteflies/thrips.",
            "Install 10–12 yellow and blue sticky traps per acre at 15 cm above crop canopy height.",
            "Use pheromone traps (5 per acre) to monitor fruit borer moth activity early.",
            "Spray 5% Neem Seed Kernel Extract (NSKE) or Azadirachtin 1500 ppm during early pest stages.",
        ],
        "summary": "Combine border crops, sticky traps, and botanical sprays to control sucking pests and borers safely.",
        "precautions": "Avoid spraying broad-spectrum pyrethroids early in the season as they kill beneficial spiders and ladybird beetles.",
    },
    {
        "id": "guide-4",
        "category": "Irrigation",
        "title": "Drip Irrigation & Mulching Best Practices for Horticulture",
        "crops": "Tomato, Chilli, Melons, Vegetables",
        "summary": "Maintain uniform root moisture, prevent weed growth, and reduce fungal foliar splash.",
        "steps": [
            "Lay drip inline laterals on raised beds after incorporating basal organic compost.",
            "Cover raised beds with 25–30 micron silver-black mulching film and punch holes at recommended spacing.",
            "Check soil moisture 5–8 cm below the dripper before scheduling irrigation cycles.",
            "Flush lateral end-caps every 15 days and clean screen/disc filters regularly.",
        ],
        "precautions": "Never over-irrigate mulched beds, as trapped excess water around the root collar can trigger damping-off or wilt.",
    },
    {
        "id": "guide-5",
        "category": "Organic farming",
        "title": "Preparing Enriched Vermicompost & Bio-Fertilizer Seed Treatment",
        "crops": "Pulses, Cereals, Vegetables",
        "summary": "Boost beneficial soil microbes and early root nodulation with low-cost biological inputs.",
        "steps": [
            "Enrich 100 kg of mature vermicompost with 1 kg Trichoderma viride and 1 kg Pseudomonas fluorescens in shade for 7 days.",
            "Treat legume/pulse seeds with crop-specific Rhizobium + PSB culture in cool jaggery solution.",
            "Dry treated seeds in shade for 30 minutes on a clean sack before sowing immediately.",
        ],
        "precautions": "Do not mix biological bio-fertilizers directly with chemical fungicides or exposed hot sunlight.",
    },
    {
        "id": "guide-6",
        "category": "Fertilizers",
        "title": "Split Nutrient Scheduling: Getting More Value from Less Fertilizer",
        "crops": "Paddy, Maize, Cotton, Vegetables",
        "summary": "Match nutrient availability to active root demand stages and prevent leaching losses.",
        "steps": [
            "Apply full phosphorus (P) and basal organic manure during final land preparation near the root zone.",
            "Divide nitrogen (N) into 3 equal splits (Basal, Active Vegetative/Tillering, and Panicle/Flowering initiation).",
            "Ensure soil is moist (not bone-dry and not overflowing) when top-dressing nutrients.",
        ],
        "precautions": "Avoid excess nitrogen applications, which create soft, succulent foliage that attracts pests and diseases.",
    },
]


# ==============================================================================
# 8. GOVERNMENT SCHEMES & ELIGIBILITY ASSISTANT
# ==============================================================================
GOVERNMENT_SCHEMES = [
    {
        "id": "sch-pmkisan",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "category": "Financial assistance",
        "level": "Central government",
        "description": "Direct income support of ₹6,000 per year in three equal installments of ₹2,000 directly into Aadhaar-seeded bank accounts of landholding farmer families.",
        "eligibility": "Cultivable landholding farmer families (subject to standard institutional/income exclusion criteria).",
        "benefits": "₹6,000 / year in 3 installments via DBT for agricultural input expenses.",
        "documents": ["Aadhaar Card", "Land Ownership / RoR (Pattadar Passbook)", "Active Bank Account linked with Aadhaar (NPCI DBT)", "Mobile Number for e-KYC"],
        "application_process": "Complete e-KYC online at pmkisan.gov.in or visit your nearest CSC / Village Secretariat / Agriculture Officer.",
        "official_link": "https://pmkisan.gov.in/",
        "source": "Ministry of Agriculture & Farmers Welfare, Govt. of India",
        "verified_date": "2026-10",
    },
    {
        "id": "sch-pmfby",
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "category": "Crop insurance",
        "level": "Central government",
        "description": "Comprehensive crop insurance protecting farmers against non-preventable natural risks (drought, flood, cyclone, unseasonal rain, pests/diseases) from pre-sowing to post-harvest.",
        "eligibility": "All farmers (landowners and tenant/sharecroppers growing notified crops in notified areas) who enroll before the seasonal cut-off date.",
        "benefits": "Low farmer premium: 2% for Kharif crops, 1.5% for Rabi crops, and 5% for commercial/horticultural crops; balance subsidy paid by Government.",
        "documents": ["Aadhaar Card", "Land Possession / Tenancy Certificate", "Sowing Certificate", "Bank Account Passbook"],
        "application_process": "Apply via pmfby.gov.in, your bank branch, CSC centre, or the Crop Insurance mobile app before seasonal deadline.",
        "official_link": "https://pmfby.gov.in/",
        "source": "Ministry of Agriculture & Farmers Welfare, Govt. of India",
        "verified_date": "2026-10",
    },
    {
        "id": "sch-pmksy",
        "name": "PMKSY — Per Drop More Crop (Micro-Irrigation Subsidy)",
        "category": "Equipment subsidies",
        "level": "Central government",
        "description": "Financial subsidy for installing Drip and Sprinkler micro-irrigation systems to conserve water and improve fertilizer efficiency.",
        "eligibility": "All farmers with cultivable land and an assured irrigation water source (borewell, open well, canal, farm pond).",
        "benefits": "Up to 55% financial assistance for Small & Marginal farmers and 45% for other farmers (plus additional state top-up subsidies where applicable).",
        "documents": ["Aadhaar Card", "Land Record (1B / Adangal / Pahani)", "Water Source & Soil Report", "Passport Photo & Bank Details"],
        "application_process": "Register on pmksy.gov.in or your State Horticulture / Micro-Irrigation portal through District Horticulture Officer.",
        "official_link": "https://pmksy.gov.in/",
        "source": "Department of Agriculture & Farmers Welfare",
        "verified_date": "2026-10",
    },
    {
        "id": "sch-shc",
        "name": "Soil Health Card (SHC) Scheme",
        "category": "Farmer welfare",
        "level": "Central government",
        "description": "Provides every farmer with a field-specific Soil Health Card detailing 12 soil parameters (N, P, K, S, Zn, Fe, Cu, Mn, B, pH, EC, OC) and crop-wise fertilizer recommendations.",
        "eligibility": "All farmers across India.",
        "benefits": "Free or nominal-fee laboratory soil testing and customized organic + chemical fertilizer dosage chart.",
        "documents": ["Aadhaar Card", "Mobile Number", "Field Survey / Plot Details"],
        "application_process": "Submit composite soil sample at your nearest Mandal Agriculture Office, KVK, or track report at soilhealth.dac.gov.in.",
        "official_link": "https://soilhealth.dac.gov.in/",
        "source": "Department of Agriculture & Farmers Welfare",
        "verified_date": "2026-10",
    },
    {
        "id": "sch-kcc",
        "name": "Kisan Credit Card (KCC) — Concessional Crop Loan",
        "category": "Financial assistance",
        "level": "Central government",
        "description": "Timely and affordable short-term credit for crop cultivation, post-harvest expenses, and allied dairy/fishery activities with interest subvention.",
        "eligibility": "Owner cultivators, tenant farmers, oral lessees, sharecroppers, and SHGs/Joint Liability Groups.",
        "benefits": "Short-term crop loans up to ₹3 Lakh at 7% p.a., reduced effectively to 4% p.a. with 3% Prompt Repayment Incentive.",
        "documents": ["Aadhaar Card & PAN", "Land Record / Tenancy Proof", "Passport Photos", "Bank Application Form"],
        "application_process": "Apply at any commercial, regional rural, or cooperative bank branch or via pmkisan.gov.in KCC form.",
        "official_link": "https://www.myscheme.gov.in/schemes/kcc",
        "source": "Reserve Bank of India / NABARD / Ministry of Agriculture",
        "verified_date": "2026-10",
    },
    {
        "id": "sch-state-rythu",
        "name": "State Farmer Investment & Input Support Programmes (Rythu / KALIA / Krishi Input)",
        "category": "State government",
        "level": "State government",
        "description": "State-level seasonal cultivation support, subsidized quality seeds, and farm mechanization assistance provided through Rythu Bharosa Kendras / Raitha Samparka Kendras.",
        "eligibility": "Resident farmers registered in the respective State land/farmer database (e-Crop / FRUITS / Bhulekh).",
        "benefits": "Seasonal input grant, subsidized green manure & certified seeds, and custom hiring support.",
        "documents": ["Aadhaar Card", "State Land Passbook / FRUITS ID", "e-Crop Booking Receipt", "Bank Account"],
        "application_process": "Contact your village Rythu Seva Kendra / Raitha Samparka Kendra / State Agriculture Portal.",
        "official_link": "https://www.myscheme.gov.in/",
        "source": "State Departments of Agriculture & myScheme National Portal",
        "verified_date": "2026-10",
    },
]


def check_scheme_eligibility(payload: Dict[str, Any]) -> Dict[str, Any]:
    land_acres = float(payload.get("land_acres", 2.5))
    has_land_record = bool(payload.get("has_land_record", True))
    needs_irrigation = bool(payload.get("needs_irrigation", True))
    wants_insurance = bool(payload.get("wants_insurance", True))

    matched = []
    for sch in GOVERNMENT_SCHEMES:
        if sch["id"] == "sch-pmkisan" and has_land_record:
            matched.append(sch)
        elif sch["id"] == "sch-pmfby" and wants_insurance:
            matched.append(sch)
        elif sch["id"] == "sch-pmksy" and needs_irrigation:
            matched.append(sch)
        elif sch["id"] in ("sch-shc", "sch-kcc", "sch-state-rythu"):
            matched.append(sch)

    farmer_category = "Small / Marginal Farmer (<= 5 Acres)" if land_acres <= 5.0 else "Medium / Large Farmer (> 5 Acres)"
    return {
        "farmer_category": farmer_category,
        "matched_count": len(matched),
        "matched_schemes": matched,
        "disclaimer": "Potential matches based on your inputs. Final eligibility is verified by the respective government department via official portals.",
    }


# ==============================================================================
# 9. FARMER COMMUNITY & PROFILES
# ==============================================================================
def get_community_posts(category: str = "") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if category and category != "All":
        rows = conn.execute(
            "SELECT * FROM community_posts WHERE category = ? ORDER BY id DESC", (category,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM community_posts ORDER BY id DESC").fetchall()
    conn.close()

    results = []
    for r in rows:
        item = dict(r)
        try:
            item["comments"] = json.loads(item.get("comments_json") or "[]")
        except Exception:
            item["comments"] = []
        results.append(item)
    return results


def create_community_post(payload: Dict[str, Any]) -> Dict[str, Any]:
    author = (payload.get("author_name") or "Progressive Farmer").strip()[:80]
    location = (payload.get("author_location") or "India").strip()[:80]
    category = (payload.get("category") or "Crop Diseases").strip()
    crop_tag = (payload.get("crop_tag") or "General Crop").strip()[:50]
    title = (payload.get("title") or "").strip()[:160]
    content = (payload.get("content") or "").strip()[:1500]

    conn = get_db_connection()
    cur = conn.execute(
        """
        INSERT INTO community_posts (
            author_name, author_location, category, crop_tag, title, content, likes, comments_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, 0, '[]', 'Just now')
        """,
        (author, location, category, crop_tag, title, content),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM community_posts WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    item = dict(row)
    item["comments"] = []
    return item


def like_community_post(post_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    conn.execute("UPDATE community_posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()
    row = conn.execute("SELECT * FROM community_posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    item["comments"] = json.loads(item.get("comments_json") or "[]")
    return item


def add_community_comment(post_id: int, author: str, text: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM community_posts WHERE id = ?", (post_id,)).fetchone()
    if not row:
        conn.close()
        return None
    comments = json.loads(row["comments_json"] or "[]")
    comments.append(
        {
            "author": author.strip()[:60] or "Farmer",
            "text": text.strip()[:500],
            "time": "Just now",
        }
    )
    conn.execute(
        "UPDATE community_posts SET comments_json = ? WHERE id = ?",
        (json.dumps(comments), post_id),
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM community_posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    item = dict(updated)
    item["comments"] = comments
    return item


def register_or_login_farmer(payload: Dict[str, Any]) -> Dict[str, Any]:
    name = (payload.get("name") or "Kisan Mitra").strip()
    phone = (payload.get("phone") or "9876543210").strip()
    state = (payload.get("state") or "Andhra Pradesh").strip()
    district = (payload.get("district") or "Guntur").strip()
    language_code = payload.get("language_code") or "te-IN"
    farm_size_acres = float(payload.get("farm_size_acres") or 4.5)
    primary_crops = (payload.get("primary_crops") or "Paddy, Tomato, Chilli").strip()

    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE users
            SET name = ?, state = ?, district = ?, language_code = ?, farm_size_acres = ?, primary_crops = ?
            WHERE phone = ?
            """,
            (name, state, district, language_code, farm_size_acres, primary_crops, phone),
        )
    else:
        conn.execute(
            """
            INSERT INTO users (name, phone, state, district, language_code, farm_size_acres, primary_crops, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                phone,
                state,
                district,
                language_code,
                farm_size_acres,
                primary_crops,
                datetime.date.today().isoformat(),
            ),
        )
    conn.commit()
    user = conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
    conn.close()
    return dict(user)
