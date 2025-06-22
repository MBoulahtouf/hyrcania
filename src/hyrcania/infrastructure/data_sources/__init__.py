"""
Data sources for spectroscopy data loading.
Implements strategy pattern for different spectroscopy types.
"""

from .base import SpectroscopyStrategy
from .fluorescence import FluorescenceStrategy
from .absorption import AbsorptionStrategy

__all__ = [
    'SpectroscopyStrategy',
    'FluorescenceStrategy', 
    'AbsorptionStrategy'
] 