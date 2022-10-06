
from datetime import datetime

from pydantic import (
    BaseModel,
    IPvAnyAddress,
    NonNegativeInt,
    StrictStr,
)


class SelfRegisterRequest(BaseModel):
    name: StrictStr
    port: NonNegativeInt
    expire: NonNegativeInt


class RegistryEntry(BaseModel):
    ip: IPvAnyAddress
    port: NonNegativeInt
    expire: NonNegativeInt
    expire_at: datetime | None
