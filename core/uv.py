from __future__ import annotations

import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_uv_data(lat: float, lon: float, timezone: str) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "uv_index,cloud_cover",
        "timezone": timezone,
        "forecast_days": 1,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(OPEN_METEO_URL, params=params)
        resp.raise_for_status()
        return resp.json()


def parse_uv_window(data: dict) -> list[tuple[int, float]]:
    """Return (hour, uv_index) pairs for hours with UV >= 3."""
    times = data["hourly"]["time"]
    uvs = data["hourly"]["uv_index"]
    return [
        (int(t[11:13]), uv)
        for t, uv in zip(times, uvs)
        if uv is not None and uv >= 3
    ]


def get_peak_uv(data: dict) -> float:
    uvs = [u for u in data["hourly"]["uv_index"] if u is not None]
    return max(uvs) if uvs else 0.0


def get_avg_cloud_cover_in_window(data: dict) -> float | None:
    times = data["hourly"]["time"]
    uvs = data["hourly"]["uv_index"]
    clouds = data["hourly"].get("cloud_cover", [None] * len(times))
    in_window = [c for t, uv, c in zip(times, uvs, clouds) if uv and uv >= 3 and c is not None]
    return sum(in_window) / len(in_window) if in_window else None


def format_window(window: list[tuple[int, float]]) -> str | None:
    if not window:
        return None
    start = window[0][0]
    end = window[-1][0]
    return f"{start:02d}:00 – {end + 1:02d}:00"


async def geocode_city(city_name: str) -> dict | None:
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1, "addressdetails": 1}
    headers = {"User-Agent": "SunDoseBot/1.0"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        results = resp.json()
    if not results:
        return None
    r = results[0]
    addr = r.get("address", {})
    city = (
        addr.get("city")
        or addr.get("town")
        or addr.get("village")
        or r.get("display_name", "").split(",")[0]
    )
    country = addr.get("country", "")
    return {
        "city": city,
        "country": country,
        "display": f"{city}, {country}" if country else city,
        "lat": float(r["lat"]),
        "lon": float(r["lon"]),
    }


def get_timezone(lat: float, lon: float) -> str:
    from timezonefinder import TimezoneFinder
    tf = TimezoneFinder()
    tz = tf.timezone_at(lat=lat, lng=lon)
    return tz or "UTC"
