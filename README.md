
# RNG Microservice

This service exposes one endpoint to generate stop indices for each reel. Deterministic runs are supported via an optional `seed` field.

## Files
- `rng_microservice.py` — FastAPI microservice with `/reels/spin`.

## Run the service
```bash
uvicorn rng_service_min:app --host 127.0.0.1 --port 8088 --reload
```

## Endpoint
- `POST /reels/spin`
  - Body: `{ "strip_lengths": [100,100,100,100,100], "seed": 123 }`
  - Response: `{ "stops": [23,4,59,88,17], "seed": 123 }`

## Notes
- Uses Python's `random.Random` for uniform sampling.
- For reproducible tests, pass a `seed`.
```
