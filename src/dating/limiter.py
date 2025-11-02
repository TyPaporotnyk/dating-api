from slowapi import Limiter
from slowapi.util import get_remote_address

from dating.config import REDIS_URL

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL,
    in_memory_fallback_enabled=True,
    strategy="moving-window",
    headers_enabled=False,
    default_limits=["100/minute"],
)
