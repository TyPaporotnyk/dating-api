from dataclasses import dataclass, field

from dating.mediator.commands.entities import BaseCommand
from dating.mediator.commands.handlers import BaseCommandHandler


@dataclass
class CommandMediator:
    commands_map: dict[type[BaseCommand], BaseCommandHandler] = field(default_factory=dict)

    def register_command(self, command: type[BaseCommand], command_handlers: BaseCommandHandler):
        self.commands_map[command] = command_handlers

    async def handle_command(self, command: BaseCommand):
        command_type = command.__class__
        handler = self.commands_map.get(command_type)

        if not handler:
            raise ValueError("Command handlers not registered error")

        return await handler.handle(command)
