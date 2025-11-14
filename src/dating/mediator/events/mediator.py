from collections import defaultdict
from dataclasses import dataclass, field

from dating.mediator.events.entities import BaseEvent
from dating.mediator.events.handlers import BaseEventHandler


@dataclass
class EventMediator:
    events_map: dict[type[BaseEvent], list[BaseEventHandler]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def register_events(self, event: type[BaseEvent], handlers: list[BaseEventHandler]):
        self.events_map[event] = handlers

    async def publish(self, events: list[BaseEvent]):
        result = []

        for event in events:
            handlers = self.events_map[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])

        return result
