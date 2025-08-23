from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import hmac, hashlib
import json
import time

webhook_router = APIRouter()
webhookSecret = b"pokemon"
replayWindow = 300
processedEvents = set()

@webhook_router.post("/payment")
async def payment_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    bodyBytes = await request.body()

    receivedSign = request.headers.get("X-Signature")

    if not receivedSign:
        raise HTTPException(status_code=400, detail="Missing signature header")

    computerSign = hmac.new(webhookSecret, bodyBytes, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(receivedSign, computerSign):
        raise HTTPException(status_code=401, detail="Invalid Signature")
    
    payload = json.loads(bodyBytes)
    event_id = payload.get("event_id")
    order_id = payload.get("order_id")
    event_type = payload.get("type")
    timestamp = payload.get("timestamp", int(time.time()))

    if event_id in processedEvents or abs(int(time.time() - timestamp)) > replayWindow:
        raise HTTPException(status_code=409, detail="Duplicate or expired event")
    processedEvents.add(event_id)

    if event_type == "payment.succeeded":
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = "PAID"
        db.commit()
        db.refresh(order)
        return{"status": "success", "order_id": order_id}
    
    return{"status": "ignored", "status": "Unhandled event type"}