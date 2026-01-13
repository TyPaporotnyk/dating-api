from dataclasses import dataclass

from dating.mediator.commands.mediator import CommandMediator
from dating.mediator.events.mediator import EventMediator


@dataclass
class Mediator(CommandMediator, EventMediator): ...
