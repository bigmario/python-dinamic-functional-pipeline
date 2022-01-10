from typing import Optional, List
from pydantic import BaseModel


class DateRange(BaseModel):
    from_: Optional[int]
    to: Optional[int]


class FloatRange(BaseModel):
    from_: Optional[float]
    to: Optional[float]


class DateWithConditions(BaseModel):
    date: Optional[str]
    condition: str
    date_range: Optional[DateRange]


class IntWithConditions(BaseModel):
    value: Optional[int]
    condition: str
    range: Optional[DateRange]


class FloatWithConditions(BaseModel):
    value: Optional[float]
    condition: str
    range: Optional[FloatRange]


class LogCampaign(BaseModel):
    ...
    clicked_on_link: bool
    received_pc: bool
    opened_pc: bool


class Profile(BaseModel):
    company: Optional[str]
    score: Optional[IntWithConditions]
    gender: Optional[str]
    create_at: Optional[str]
    civil_status: Optional[str]
    age_range: Optional[DateRange]
    profession: Optional[str]
    childrens: Optional[int]
    nationality: Optional[str]
    birth_date: Optional[DateWithConditions]
    languages: Optional[List[str]]
    birthdate_month: Optional[int]
    birthday_this_month: Optional[bool]
    next_birthday: Optional[bool]
    ue_contry: Optional[List[str]]
    create_at: Optional[str]
    email: Optional[List[str]]
    birthdate: Optional[str]


class Accommodation(BaseModel):
    ...
    checking: Optional[DateWithConditions]
    checkout: Optional[DateWithConditions]
    adult_number: Optional[IntWithConditions]
    children_number: Optional[IntWithConditions]
    anticipation: Optional[IntWithConditions]
    length_of_stay: Optional[int]
    reserve_creation: Optional[DateWithConditions]
    room_code: Optional[str]
    room_revenue: Optional[FloatWithConditions]
    room_type: Optional[str]
    book_property: Optional[str]


class AppliedFilters(BaseModel):
    category_name: str
    log_campaign: LogCampaign
    profile: Profile
    accommodation: Accommodation
