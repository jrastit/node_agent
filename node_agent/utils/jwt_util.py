import os
import time
import json
import base64
import hmac
import hashlib
from typing import Dict, Any

def b64url(b: bytes) -> bytes:
    return base64.urlsafe_b64encode(b).rstrip(b'=')

def create_jwt(secret_hex: str, payload: Dict[str, Any]) -> str:
    #secret = bytes.fromhex(secret_hex)
    secret = secret_hex.encode()
    header = {"alg": "HS256", "typ": "JWT"}
    enc = lambda o: b64url(json.dumps(o, separators=(',', ':')).encode())
    msg = enc(header) + b'.' + enc(payload)
    sig = b64url(hmac.new(secret, msg, hashlib.sha256).digest())
    return (msg + b'.' + sig).decode()

def generate_tokens(secret_hex: str) -> Dict[str, str]:
    now = int(time.time())
    year = 60 * 60 * 24 * 365
    # anon_payload = {"role": "anon", "iss": "supabase", "iat": now, "exp": now + year}
    # service_payload = {"role": "service_role", "iss": "supabase", "iat": now, "exp": now + year, "service_role": True}
    anon_payload = {"role": "anon", "iss": "supabase-demo", "iat": now, "exp": now + year}
    service_payload = {"role": "service_role", "iss": "supabase-demo", "iat": now, "exp": now + year}
    return {
        "anon": create_jwt(secret_hex, anon_payload),
        "service": create_jwt(secret_hex, service_payload)
    }

def check_jwt(token: str, secret_hex: str) -> bool:
    try:
        # secret = bytes.fromhex(secret_hex)
        secret = secret_hex.encode()
        header_b64, payload_b64, sig_b64 = token.split('.')
        msg = (header_b64 + '.' + payload_b64).encode()
        expected_sig = b64url(hmac.new(secret, msg, hashlib.sha256).digest()).decode()
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '=' * (-len(payload_b64) % 4)))
        print("Payload:", payload)
        return sig_b64 == expected_sig
    except Exception:
        return False

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--secret", required=True, help="HS256 secret hex")
    parser.add_argument("--mode", choices=["generate", "check"], required=True)
    parser.add_argument("--token", help="JWT token to check")
    args = parser.parse_args()
    if args.mode == "generate":
        tokens = generate_tokens(args.secret)
        print(tokens["anon"])
        print(tokens["service"])
    elif args.mode == "check":
        if not args.token:
            print("--token required for check mode", file=sys.stderr)
            sys.exit(1)
        print("valid" if check_jwt(args.token, args.secret) else "invalid")
