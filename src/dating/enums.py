from enum import StrEnum


class DatingEnum(StrEnum):
    pass


class Gender(DatingEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
