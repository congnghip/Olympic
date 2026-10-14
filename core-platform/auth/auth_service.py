"""
DX-OS Open-Core: Headless Identity & Security Module (Tầng 1)
Quản trị định danh tập trung (SSO/JWT), Kiểm soát quyền truy cập theo vai trò (RBAC).
"""

import time
import hmac
import hashlib
import base64
import json
from typing import Dict, Any, Optional

SECRET_KEY = "dx-os-open-core-super-secret-key-2026"

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

class DXAuthService:
    @staticmethod
    def create_access_token(user_id: str, username: str, role: str, expires_in_sec: int = 86400) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": user_id,
            "username": username,
            "role": role,
            "iat": int(time.time()),
            "exp": int(time.time()) + expires_in_sec,
            "iss": "dx-os-open-core"
        }
        
        header_b64 = base64url_encode(json.dumps(header).encode('utf-8'))
        payload_b64 = base64url_encode(json.dumps(payload).encode('utf-8'))
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        
        signature = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
        signature_b64 = base64url_encode(signature)
        
        return f"{header_b64}.{payload_b64}.{signature_b64}"

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            header_b64, payload_b64, signature_b64 = parts
            signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
            expected_sig = base64url_encode(hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest())
            
            if not hmac.compare_digest(signature_b64, expected_sig):
                return None
            
            payload = json.loads(base64url_decode(payload_b64).decode('utf-8'))
            if payload.get("exp", 0) < time.time():
                return None # Token expired
            
            return payload
        except Exception:
            return None
