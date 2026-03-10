# RNG Microservice

## Description
The RNG Microservice generates **uniform random reel stop indices** for slot machine reel strips. It allows other applications (main programs or microservices) to request random stop positions for each reel, with an optional deterministic `seed` for reproducible testing.

If a `seed` is supplied in the request, the same inputs will always yield the same outputs.

---

# Endpoints

# 1. Spin Reels
POST /reels/spin

Generates a stop index for each reel strip length provided.

Example Request:
POST /reels/spin

Body:
{
  "strip_lengths": [50, 50, 50],
  "seed": 424242
}

Example Response:
{
  "stops": [12, 7, 33],
  "seed": 424242
}

Error Example (invalid strip lengths):
{
  "detail": "strip_lengths must be a non-empty list of positive integers"
}

---

# Communication Contract

# Requesting Data
To request data from the RNG Microservice:

1. Send an HTTP `POST` request to `/reels/spin`.
2. Include a JSON body with `strip_lengths` (array of positive integers) and optional `seed` (integer).

Example (Python):
import requests

payload = {"strip_lengths": [60, 60, 60], "seed": 424242}
response = requests.post("http://127.0.0.1:8088/reels/spin", json=payload)
print(response.json())

---

# Receiving Data
The microservice responds with JSON data.

Example response format:
{
  "stops": [5, 18, 42],
  "seed": 424242
}

Example handling in Python:
data = response.json()
print("Stops:", data["stops"])   # [stop_reel_1, stop_reel_2, stop_reel_3]
print("Seed:", data.get("seed"))

---

# UML Sequence Diagram

Main Program        RNG Microservice
     |                      |
     |---- POST /reels/spin ------------------------------>|
     |                      |---- Compute random stops ----|
     |                      |<--- JSON {stops:[i0,i1,i2]} -|
     |<--- JSON Response ---|                              |

(If a seed is provided, identical requests yield identical responses.)

---

# How to Run the Microservice

1. Install dependencies:
pip install fastapi uvicorn pydantic

2. Start the server:
uvicorn rng_microservice:app --reload --port 8088

3. Open in browser:
http://127.0.0.1:8088/docs

---

# Test Program Example

import requests

BASE = "http://127.0.0.1:8088"

# Spin without seed (non-deterministic)
r = requests.post(f"{BASE}/reels/spin", json={"strip_lengths": [50, 50, 50]})
print("Spin (no seed):", r.json())

# Spin with seed (deterministic)
r = requests.post(f"{BASE}/reels/spin", json={"strip_lengths": [60, 60, 60], "seed": 424242})
print("Spin (seeded):", r.json())

---

## Notes
- All communication is done using JSON over HTTP.
- `strip_lengths` must be a non-empty list of **positive** integers.
- When `seed` is supplied, the RNG is deterministic for testability.
- API documentation is available at `/docs` (Swagger UI).
