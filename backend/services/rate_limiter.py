import os
import time
import threading
from typing import Dict, List
from fastapi import Request, HTTPException

class InMemoryRateLimiter:
    """
    Thread-safe in-memory sliding window rate limiter per client IP.
    """
    def __init__(self, default_limit: int = 20, window_seconds: int = 60):
        self.default_limit = default_limit
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._history: Dict[str, List[float]] = {}

    def get_limit(self) -> int:
        env_val = os.getenv("PROMPTSHIELD_CHAT_RATE_LIMIT")
        if env_val:
            try:
                # Handle both raw int ("20") or format ("20/minute" or "20/min")
                cleaned = env_val.split("/")[0].strip()
                return int(cleaned)
            except ValueError:
                pass
        return self.default_limit

    def check_rate_limit(self, request: Request) -> None:
        client_ip = "127.0.0.1"
        if request.client and request.client.host:
            client_ip = request.client.host
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()

        limit = self.get_limit()
        now = time.time()
        window_start = now - self.window_seconds

        with self._lock:
            timestamps = self._history.get(client_ip, [])
            # Filter out entries outside current sliding window
            valid_timestamps = [t for t in timestamps if t > window_start]

            if len(valid_timestamps) >= limit:
                oldest = valid_timestamps[0]
                retry_after = max(1, int(oldest + self.window_seconds - now))
                self._history[client_ip] = valid_timestamps
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded: maximum {limit} requests per minute.",
                    headers={"Retry-After": str(retry_after)}
                )

            valid_timestamps.append(now)
            self._history[client_ip] = valid_timestamps

    def reset(self) -> None:
        with self._lock:
            self._history.clear()

chat_limiter = InMemoryRateLimiter(default_limit=20, window_seconds=60)

async def rate_limit_chat(request: Request) -> None:
    chat_limiter.check_rate_limit(request)
