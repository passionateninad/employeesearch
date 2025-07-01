import time
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse

# Rate limiting config
RATE_LIMIT = 5  # requests
TIME_WINDOW = 60  # seconds

# Memory store: IP → request timestamps
rate_storage = defaultdict(list)

def is_rate_limited(client_ip: str) -> bool:
    now = time.time()
    requests = rate_storage[client_ip]

    # Clean up old requests
    rate_storage[client_ip] = [req for req in requests if now - req < TIME_WINDOW]

    if len(rate_storage[client_ip]) >= RATE_LIMIT:
        return True

    rate_storage[client_ip].append(now)
    return False

# FastAPI middleware
async def rate_limiter_middleware(request: Request, call_next):
    client_ip = request.client.host
    if is_rate_limited(client_ip):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."}
        )
    return await call_next(request)
