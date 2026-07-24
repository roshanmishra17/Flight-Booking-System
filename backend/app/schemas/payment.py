from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.payment import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    booking_id: int
    payment_method: PaymentMethod
    simulate_failure: bool = False
    
    model_config = ConfigDict(extra="forbid")

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: Decimal
    payment_method: PaymentMethod
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)