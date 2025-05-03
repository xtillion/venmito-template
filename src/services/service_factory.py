# src/services/service_factory.py
from typing import Dict, Any, Optional, Type

from src.services.data_processing_service import (
    DataProcessingService, 
    PeopleProcessingService,
    TransactionProcessingService,
    TransferProcessingService
)
from src.data.validator import get_validator

class ServiceFactory:
    """Factory for creating service instances."""
    
    _services: Dict[str, DataProcessingService] = {}
    
    @classmethod
    def get_service(cls, service_type: str) -> DataProcessingService:
        """
        Get a service instance by type.
        
        Args:
            service_type: The type of service to get ('people', 'transactions', 'transfers')
            
        Returns:
            An instance of the requested service
        """
        if service_type not in cls._services:
            if service_type == 'people':
                # Don't initialize validator with None
                cls._services[service_type] = PeopleProcessingService()
            elif service_type == 'transactions':
                cls._services[service_type] = TransactionProcessingService(
                    people_service=cls.get_service('people')
                )
            elif service_type == 'transfers':
                cls._services[service_type] = TransferProcessingService(
                    transaction_service=cls.get_service('transactions')
                )
            else:
                raise ValueError(f"Unknown service type: {service_type}")
        
        return cls._services[service_type]
    
    @classmethod
    def reset(cls) -> None:
        """Reset all service instances. Useful for testing."""
        cls._services = {}