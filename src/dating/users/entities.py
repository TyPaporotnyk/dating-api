from dataclasses import dataclass

from dating.entities import Entity


@dataclass
class User(Entity):
    email: str
