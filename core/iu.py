from __future__ import annotations

BASE_IU = 3000

SKIN_MULT = {1: 2.0, 2: 1.5, 3: 1.0, 4: 0.6, 5: 0.4}
AREA_MULT = {"arms": 0.6, "arms_legs": 1.0, "full": 1.4}


def estimate_iu(skin_type: int, exposed_area: str, uv_index: float, duration: int) -> int:
    skin = SKIN_MULT.get(skin_type, 1.0)
    area = AREA_MULT.get(exposed_area, 1.0)
    uv = uv_index / 6
    time = min(duration / 20, 1.5)
    return int(BASE_IU * skin * area * uv * time)
