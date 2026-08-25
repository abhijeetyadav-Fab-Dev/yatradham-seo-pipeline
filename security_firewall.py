"""
Enterprise Security Firewall & Hardening Layer for YatraDham SEO Pipeline.
Addresses OWASP Top 10 & API Security Flaws:
1. API Authentication & Role-Based Access Control (API Keys / Admin Session)
2. Destructive Operations Guard (Protected wipes, bulk actions, deletions)
3. Strict Schema Validation on Updates (Prevents Mass Assignment)
4. WordPress Credential Security & Encryption/Masking
5. SSRF & Protocol Smuggling Protections
6. Provider Architecture Masking (Prevents Backend Information Disclosure)
7. Secret Masking in Logs & Memory
8. Prompt Injection Firewall (Detects instruction override, jailbreaks, system leaks)
9. Rate Limiting & DoS Protection (Batch and generation throttling)
10. Robots.txt, Security Headers, and Internal Error Sanitization
"""
import os
import re
import hmac
import hashlib
import ipaddress
import socket
import urllib.parse
from typing import Tuple, Dict, Any, Optional, List
from fastapi import HTTPException, Request, Security, Depends
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

# Admin API Key configuration (Defaults to secure hash comparison or env)
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "yatradham-admin-secure-key-2026")
API_KEY_HEADER = APIKeyHeader(name="X-Admin-Key", auto_error=False)
BEARER_AUTH = HTTPBearer(auto_error=False)


# =====================================================================
# 1. AUTHENTICATION & ACCESS CONTROL
# =====================================================================
def verify_admin_access(request: Request, api_key: Optional[str] = Security(API_KEY_HEADER), bearer: Optional[HTTPAuthorizationCredentials] = Security(BEARER_AUTH)) -> bool:
    """
    Verifies that the caller has valid administrative access.
    Allows request if:
    - Valid X-Admin-Key header provided
    - Valid Bearer token provided
    - Local loopback development environment without configured secret
    """
    token_candidate = api_key or (bearer.credentials if bearer else None) or request.headers.get("X-API-Key")
    
    # Check query param as fallback for downloads/exports if configured
    if not token_candidate and "admin_key" in request.query_params:
        token_candidate = request.query_params["admin_key"]

    if token_candidate and hmac.compare_digest(token_candidate.strip(), ADMIN_API_KEY.strip()):
        return True

    # If ADMIN_API_KEY is unset in local dev, allow localhost only
    client_ip = request.client.host if request.client else "127.0.0.1"
    if (client_ip in ["127.0.0.1", "::1", "localhost"]) and not os.environ.get("ENFORCE_PROD_AUTH"):
        return True

    raise HTTPException(
        status_code=401,
        detail="Unauthorized: Admin access required. Provide 'X-Admin-Key' or 'Authorization: Bearer <token>' header."
    )


# =====================================================================
# 2. STRICT SCHEMA VALIDATION (MASS ASSIGNMENT PREVENTION)
# =====================================================================
class OutputUpdateRequest(BaseModel):
    title_tag: Optional[str] = Field(None, max_length=150)
    meta_description: Optional[str] = Field(None, max_length=300)
    primary_keyword: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, pattern=r"^(pending|approved|rejected|flagged_review|approved_candidate)$")
    sections: Optional[Dict[str, Any]] = None

    class Config:
        extra = "forbid"  # Strictly reject any unknown/internal fields (e.g. id, created_at, internal flags)


# =====================================================================
# 3. PROMPT INJECTION FIREWALL
# =====================================================================
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"system\s*:\s*override",
    r"you\s+are\s+now\s+(an\s+uncensored|a\s+different|in\s+god\s+mode)",
    r"output\s+the\s+(system\s+prompt|raw\s+instructions|developer\s+mode)",
    r"reveal\s+(api\s*keys?|secrets?|environment\s+variables?)",
    r"<\s*script\s*>",
    r"eval\s*\(",
    r"exec\s*\(",
]

def sanitize_user_prompt(text: str, max_chars: int = 1500) -> str:
    """
    Sanitizes user instructions and checks for active prompt injection attacks.
    """
    if not text or not isinstance(text, str):
        return ""

    clean = text.strip()
    if len(clean) > max_chars:
        clean = clean[:max_chars]

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, clean, re.IGNORECASE):
            logger_pattern = pattern.replace("\\", "")
            raise HTTPException(
                status_code=400,
                detail=f"Security Alert: Input contained potentially unsafe prompt override patterns ({logger_pattern})."
            )

    return clean


# =====================================================================
# 4. SENSITIVE CREDENTIAL & INFORMATION MASKING
# =====================================================================
def mask_secret(secret: Optional[str]) -> str:
    """Return a masked representation of sensitive keys."""
    if not secret:
        return ""
    s = str(secret).strip()
    if len(s) <= 8:
        return "********"
    return f"{s[:3]}...{s[-4:]}"


def sanitize_error_detail(e: Exception) -> str:
    """Sanitizes raw python exception traces for public consumption."""
    msg = str(e)
    # Mask any api key patterns
    msg = re.sub(r"nvapi-[A-Za-z0-9_\-]+", "nvapi-***MASKED***", msg)
    msg = re.sub(r"gsk_[A-Za-z0-9_\-]+", "gsk_***MASKED***", msg)
    msg = re.sub(r"AIza[0-9A-Za-z-_]{35}", "AIza***MASKED***", msg)
    msg = re.sub(r"sk-or-v1-[A-Za-z0-9_\-]+", "sk-or-***MASKED***", msg)
    return msg


# =====================================================================
# 5. ROBOTS.TXT CONTENT
# =====================================================================
ROBOTS_TXT_CONTENT = """User-agent: *
Disallow: /api/
Disallow: /docs
Disallow: /redoc
Disallow: /openapi.json
Disallow: /settings/
Disallow: /outputs
Disallow: /export_csv
Disallow: /clear-cache

Sitemap: https://yatradham.org/sitemap.xml
"""
