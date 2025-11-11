#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C

# ---------- helpers ----------
rand_hex() {           # N bytes -> hex (2N chars)
  openssl rand -hex "$1"
}
rand_b64_bytes() {     # N bytes -> base64 (single line)
  openssl rand -base64 "$1" | tr -d '\n'
}
rand_alnum() {         # N alnum chars, robust on macOS/BSD
  local n="$1" out=""
  while [ "${#out}" -lt "$n" ]; do
    local need=$(( n - ${#out} ))
    local chunk
    chunk="$(openssl rand -base64 $((need*2 + 16)) | LC_ALL=C tr -dc 'A-Za-z0-9' | head -c "$need" || true)"
    out="${out}${chunk}"
  done
  printf '%s' "$out"
}

# ---------- generate values ----------
POSTGRES_PASSWORD="$(rand_alnum 16)"                  # 16 alnum
JWT_SECRET_HEX="$(rand_hex 32)"                       # 32 bytes -> 64 hex chars (HS256 secret)
SECRET_KEY_BASE="$(rand_hex 32)"                      # 32 bytes -> 64 hex chars
VAULT_ENC_KEY="$(rand_hex 16)"                        # 16 bytes -> 32 hex chars (raw 32 chars total)
PG_META_CRYPTO_KEY="$(rand_b64_bytes 32)"             # base64(32 bytes)
DASHBOARD_USERNAME="$(rand_alnum 8)"
DASHBOARD_PASSWORD="$(rand_alnum 16)"

# ---------- generate JWTs (Anon / Service Role) ----------
# Uses Python stdlib only; signs with HS256 using JWT_SECRET_HEX.
export JWT_SECRET_HEX
readarray -t JWT_KEYS < <(python3 - <<'PY'
import os, time, json, base64, hmac, hashlib, sys

secret_hex = os.environ.get("JWT_SECRET_HEX")
if not secret_hex:
  print("ERROR: JWT_SECRET_HEX not set", file=sys.stderr)
  sys.exit(1)
secret = bytes.fromhex(secret_hex)

def b64url(b: bytes) -> bytes:
  return base64.urlsafe_b64encode(b).rstrip(b'=')

def jwt(payload: dict) -> str:
  header = {"alg":"HS256","typ":"JWT"}
  enc = lambda o: b64url(json.dumps(o, separators=(',',':')).encode())
  msg = enc(header) + b'.' + enc(payload)
  sig = b64url(hmac.new(secret, msg, hashlib.sha256).digest())
  return (msg + b'.' + sig).decode()

now = int(time.time())
year = 60*60*24*365
anon = jwt({"role":"anon","iss":"supabase","iat":now,"exp":now+year})
service = jwt({"role":"service_role","iss":"supabase","iat":now,"exp":now+year,"service_role":True})
print(anon)
print(service)
PY
)
ANON_KEY="${JWT_KEYS[0]}"
SERVICE_ROLE_KEY="${JWT_KEYS[1]}"

# ---------- write .env.local ----------
cat > .env.local <<ENV
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
JWT_SECRET=$JWT_SECRET_HEX
ANON_KEY=$ANON_KEY
SERVICE_ROLE_KEY=$SERVICE_ROLE_KEY
DASHBOARD_USERNAME=$DASHBOARD_USERNAME
DASHBOARD_PASSWORD=$DASHBOARD_PASSWORD
SECRET_KEY_BASE=$SECRET_KEY_BASE
VAULT_ENC_KEY=$VAULT_ENC_KEY
PG_META_CRYPTO_KEY=$PG_META_CRYPTO_KEY
ENV

echo "✅ Generated .env.local"
cat .env.local

# ---------- sanity checks ----------
echo
echo "Sanity checks:"
awk -F= '/^VAULT_ENC_KEY=/{print "VAULT_ENC_KEY length:", length($2)}' .env.local   # expect 32
awk -F= '/^PG_META_CRYPTO_KEY=/{print $2}' .env.local | awk '{l=length($0)%4; if(l>0) printf "%s%s\n", $0, substr("====",1,4-l); else print $0}' | base64 -d | wc -c | xargs echo "PG_META_CRYPTO_KEY bytes:"
awk -F= '/^POSTGRES_PASSWORD=/{print "POSTGRES_PASSWORD length:", length($2)}' .env.local   # expect 16
awk -F= '/^JWT_SECRET=/{print "JWT_SECRET_HEX length:", length($2)}' .env.local             # expect 64
awk -F= '/^SECRET_KEY_BASE=/{print "SECRET_KEY_BASE length:", length($2)}' .env.local       # expect 64
awk -F= '/^ANON_KEY=/{print "ANON_KEY length:", length($2)}' .env.local                     # JWT, variable length
awk -F= '/^SERVICE_ROLE_KEY=/{print "SERVICE_ROLE_KEY length:", length($2)}' .env.local     # JWT, variable length
awk -F= '/^DASHBOARD_USERNAME=/{print "DASHBOARD_USERNAME length:", length($2)}' .env.local         # expect 8
awk -F= '/^DASHBOARD_PASSWORD=/{print "DASHBOARD_PASSWORD length:", length($2)}' .env.local # expect 16

export ANON_KEY
export JWT_SECRET_HEX
export SERVICE_ROLE_KEY

python3 - <<'PY'
import os, jwt, binascii

def check_token(token_env, secret_env):
    token = os.environ.get(token_env)
    secret_raw = os.environ.get(secret_env)

    if not token or not secret_raw:
        print(f"❌ Please set {token_env} and {secret_env} env vars")
        return

    try:
        secret = bytes.fromhex(secret_raw)
    except (binascii.Error, ValueError):
        secret = secret_raw.encode()

    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        print(f"✅ {token_env} is valid!")
        print(decoded)
    except jwt.ExpiredSignatureError:
        print(f"❌ {token_env} has expired")
    except jwt.InvalidSignatureError:
        print(f"❌ Invalid signature — wrong secret for {token_env}")
    except Exception as e:
        print(f"❌ Other error for {token_env}:", e)

check_token("ANON_KEY", "JWT_SECRET_HEX")
check_token("SERVICE_ROLE_KEY", "JWT_SECRET_HEX")
PY
