from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from dating.mediator.events.entities import BaseEvent

ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass
class BaseEventHandler(ABC, Generic[ET, ER]):
    @abstractmethod
    async def handle(self, event: ET) -> ER: ...
