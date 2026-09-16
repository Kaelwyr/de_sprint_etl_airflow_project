import pydantic
from datetime import datetime


class CustomerResearchModel(pydantic.BaseModel):
    date_id: datetime
    category_id: int
    geo_id: int
    sales_qty: int
    sales_amt: int