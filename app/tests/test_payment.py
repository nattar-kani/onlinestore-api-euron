import hmac, hashlib

payload = b'{"status": "PAID", "order_id": 1002}' 
secret = b"pokemon"

signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
print(signature)
