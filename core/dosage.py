from __future__ import annotations

BASE_MINUTES: dict[int, dict[str, int]] = {
    1: {"arms": 15, "arms_legs": 10, "full": 7},
    2: {"arms": 20, "arms_legs": 14, "full": 10},
    3: {"arms": 30, "arms_legs": 20, "full": 14},
    4: {"arms": 50, "arms_legs": 33, "full": 23},
    5: {"arms": 70, "arms_legs": 47, "full": 33},
}

MAX_MINUTES = 30


def calculate_exposure(skin_type: int, exposed_area: str, uv_index: float) -> int:
    base = BASE_MINUTES.get(skin_type, BASE_MINUTES[3]).get(exposed_area, 20)
    if uv_index <= 0:
        return MAX_MINUTES
    minutes = base / (uv_index / 3)
    return min(int(round(minutes)), MAX_MINUTES)


def adjust_for_clouds(minutes: int, cloud_cover: float | None) -> tuple[int, bool]:
    """Return (adjusted_minutes, was_adjusted). Doubles time if clouds > 80%."""
    if cloud_cover is not None and cloud_cover > 80:
        return min(minutes * 2, 60), True
    return minutes, False
