from typing import Literal
from pydantic import BaseModel


class NSFWCheckResponse(BaseModel):
    status: Literal["OK", "REJECTED"]
    reason: str | None = None