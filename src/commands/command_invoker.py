# src/commands/command_invoker.py
from typing import List, Dict, Any

from src.commands.command import Command


class CommandInvoker:
    """Invoker for executing commands."""
    
    def __init__(self):
        """Initialize the invoker."""
        self.command_history: List[Command] = []
    
    def execute_command(self, command: Command) -> Any:
        """
        Execute a command and add it to the history.
        
        Args:
            command: The command to execute
            
        Returns:
            The result of the command execution
        """
        result = command.execute()
        self.command_history.append(command)
        return result
    
    def get_history(self) -> List[Command]:
        """
        Get the command history.
        
        Returns:
            The list of executed commands
        """
        return self.command_history.copy()