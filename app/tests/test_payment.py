import hmac, hashlib, json, time

payload_dict = {
    "event_id": "evt_12345",
    "order_id": 2002,
    "type": "payment.succeeded",
    "timestamp": int(time.time())
}
payload = json.dumps(payload_dict, separators=(',', ':')).encode("utf-8")

secret = b"pokemon"
signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()

print("Payload:", payload.decode())
print("Signature:", signature)