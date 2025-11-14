import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple

_cache = {}
CACHE_TTL_SECONDS = 300  # 5 minutes

def generate_cache_key(pdf_content: bytes, question: str) -> str:
    content_hash = hashlib.md5(pdf_content).hexdigest()
    question_hash = hashlib.md5(question.encode()).hexdigest()
    return f"{content_hash}_{question_hash}"

def get_cache(key: str) -> Optional[str]:
    _clean_expired()
    if key in _cache:
        value, timestamp = _cache[key]
        if datetime.utcnow() - timestamp < timedelta(seconds=CACHE_TTL_SECONDS):
            return value
        del _cache[key]
    return None

def set_cache(key: str, value: str):
    _cache[key] = (value, datetime.utcnow())

def _clean_expired():
    now = datetime.utcnow()
    expired_keys = [
        k for k, (_, ts) in _cache.items()
        if now - ts > timedelta(seconds=CACHE_TTL_SECONDS)
    ]
    for k in expired_keys:
        del _cache[k]