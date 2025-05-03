# src/commands/command.py
from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """Base command interface."""
    
    @abstractmethod
    def execute(self) -> Any:
        """Execute the command and return the result."""
        pass