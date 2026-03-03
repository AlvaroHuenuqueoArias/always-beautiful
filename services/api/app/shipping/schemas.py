from pydantic import BaseModel


class Address(BaseModel):
    name: str
    email: str
    street: str
    number: str
    comuna: str
    city: str
    region: str
    country: str = "CL"
    phone: str


class Parcel(BaseModel):
    weight_kg: float
    length_cm: float
    width_cm: float
    height_cm: float


class ShippingRateRequest(BaseModel):
    to_address: Address
    parcel: Parcel


class ShippingRateOption(BaseModel):
    provider: str
    service: str
    price: float
    currency: str = "CLP"


class ShippingRateResponse(BaseModel):
    options: list[ShippingRateOption]
    selected: ShippingRateOption | None = None