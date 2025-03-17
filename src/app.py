import os
import uuid
from typing import Dict

import requests
from fastapi import FastAPI, HTTPException

from models import Payment

app = FastAPI()

# In-memory order store
payments: Dict[str, Payment] = {}

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://orders-svc.api")


@app.get("/healthz", status_code=201)
async def health():
    return {"message": "Hi Mom!"}


@app.post("/payments", response_model=Payment)
def process_payment(payment: Payment):
    payment.id = str(uuid.uuid4())
    payments[payment.id] = payment

    # After payment, update the order status in Orders Service
    update_order_url = f"{ORDER_SERVICE_URL}/orders/{payment.order_id}/status"
    response = requests.patch(update_order_url, params={"status": "paid"})
    if not response.status_code == 200:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    payment.status = "paid"
    return payment


@app.get("/payments/{payment_id}", response_model=Payment)
def get_payment(payment_id: str):
    if payment_id not in payments:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payments[payment_id]
