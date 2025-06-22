"""
Factory pattern for creating spectroscopy data sources.
"""

from typing import Dict, Type
from pathlib import Path

from hyrcania.domain.models.spectrum import SpectroscopyType
from .fluorescence import FluorescenceStrategy
from .absorption import AbsorptionStrategy


class SpectroscopyDataSourceFactory:
    """Factory for creating spectroscopy data source strategies."""
    
    _strategies: Dict[SpectroscopyType, Type] = {
        SpectroscopyType.FLUORESCENCE: FluorescenceStrategy,
        SpectroscopyType.ABSORPTION: AbsorptionStrategy,
    }
    
    @classmethod
    def create_strategy(cls, spectroscopy_type: SpectroscopyType):
        """
        Create a spectroscopy strategy based on type.
        
        Args:
            spectroscopy_type: Type of spectroscopy
            
        Returns:
            Spectroscopy strategy instance
        """
        if spectroscopy_type not in cls._strategies:
            raise ValueError(f"Unsupported spectroscopy type: {spectroscopy_type}")
        
        strategy_class = cls._strategies[spectroscopy_type]
        return strategy_class()
    
    @classmethod
    def create_strategy_from_file(cls, file_path: Path):
        """
        Create a spectroscopy strategy based on file path.
        
        Args:
            file_path: Path to the spectroscopy data file
            
        Returns:
            Spectroscopy strategy instance
        """
        # Determine spectroscopy type from file path
        if "Fluorescence" in str(file_path):
            return cls.create_strategy(SpectroscopyType.FLUORESCENCE)
        elif "Absorption" in str(file_path):
            return cls.create_strategy(SpectroscopyType.ABSORPTION)
        else:
            # Default to fluorescence for now
            return cls.create_strategy(SpectroscopyType.FLUORESCENCE)
    
    @classmethod
    def register_strategy(cls, spectroscopy_type: SpectroscopyType, strategy_class: Type):
        """
        Register a new spectroscopy strategy.
        
        Args:
            spectroscopy_type: Type of spectroscopy
            strategy_class: Strategy class to register
        """
        cls._strategies[spectroscopy_type] = strategy_class 