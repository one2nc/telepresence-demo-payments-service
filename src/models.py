from pydantic import BaseModel


class Payment(BaseModel):
    id: str = ""
    user_id: str
    order_id: str
    amount: float
    status: str = ""
