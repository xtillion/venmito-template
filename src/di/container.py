# src/di/container.py
from typing import Dict, Any, Type, Optional, Callable

class DIContainer:
    """Simple dependency injection container."""
    
    _instances: Dict[str, Any] = {}
    _factories: Dict[str, Callable[[], Any]] = {}
    
    @classmethod
    def register_instance(cls, key: str, instance: Any) -> None:
        """
        Register an instance for a key.
        
        Args:
            key: The key to register the instance under
            instance: The instance to register
        """
        cls._instances[key] = instance
    
    @classmethod
    def register_factory(cls, key: str, factory: Callable[[], Any]) -> None:
        """
        Register a factory function for a key.
        
        Args:
            key: The key to register the factory under
            factory: The factory function to create the instance
        """
        cls._factories[key] = factory
    
    @classmethod
    def get(cls, key: str) -> Any:
        """
        Get an instance for a key.
        
        Args:
            key: The key to get the instance for
            
        Returns:
            The instance for the key
            
        Raises:
            KeyError: If the key is not registered
        """
        if key in cls._instances:
            return cls._instances[key]
        
        if key in cls._factories:
            instance = cls._factories[key]()
            cls._instances[key] = instance
            return instance
        
        raise KeyError(f"No instance or factory registered for key: {key}")
    
    @classmethod
    def reset(cls) -> None:
        """Reset the container. Useful for testing."""
        cls._instances = {}
        cls._factories = {}