import time
from collections import defaultdict

RATE_LIMIT = 5  # max 5 requests
TIME_WINDOW = 60  # seconds

rate_storage = defaultdict(list)

def is_rate_limited(client_ip: str) -> bool:
    now = time.time()
    requests = rate_storage[client_ip]

    # Remove outdated requests
    rate_storage[client_ip] = [req for req in requests if now - req < TIME_WINDOW]

    if len(rate_storage[client_ip]) >= RATE_LIMIT:
        return True

    rate_storage[client_ip].append(now)
    return False
