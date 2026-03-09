"""
RNG Microservice

Features:
- POST /reels/spin   → returns stop indexes for each reel strip (uniform random)
- Optional deterministic seeding via JSON payload: {"seed": <int>}
- Minimal validation for strip length correctness
- Automatically compatible with seed‑based testing for reproducible slot outcomes
- Swagger /docs UI automatically available (FastAPI)

Run:
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install fastapi uvicorn pydantic
  uvicorn rng_microservice:app --host 127.0.0.1 --port 8088 --reload

Notes:
- Default engine uses Python’s `random.Random()` for simple uniform sampling.
- When a seed is provided, the service uses deterministic Mersenne Twister output.
- Purpose-built for slot machine reel-stop generation; not an all-purpose RNG.
- Extremely small surface area → ideal for CS361 microservice requirements.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="RNG Microservice", version="0.1.0")

class SpinRequest(BaseModel):
    strip_lengths: list[int]
    seed: int | None = None

@app.post("/reels/spin")
def reels_spin(body: SpinRequest):
    if not body.strip_lengths or any(L <= 0 for L in body.strip_lengths):
        raise HTTPException(status_code=400, detail="strip_lengths must be a non-empty list of positive integers")
    rng = random.Random(body.seed) if body.seed is not None else random.Random()
    stops = [rng.randrange(L) for L in body.strip_lengths]
    return {"stops": stops, "seed": body.seed}
