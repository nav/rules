import typing
import datetime
from pydantic import BaseModel


class Organization(BaseModel):
    name: str


class Person(BaseModel):
    organization: Organization
    age: int
    sex_at_birth: typing.Literal["male", "female"]
    address_state: str
    address_country: str


class Product(BaseModel):
    sku: str
    name: str
    available_until: datetime.datetime
    available_in_states: typing.List[str]


class Questionnaire(BaseModel):
    are_you_pregnant: bool


class Fact(BaseModel):
    person: Person
    questionnaire: typing.Optional[Questionnaire] = None
    product: typing.Optional[Product] = None
