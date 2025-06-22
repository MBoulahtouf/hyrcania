"""
Domain models for the Hyrcania spectroscopy project.
Contains core scientific data structures and business logic.
"""

from .spectrum import Spectrum, SpectralData
from .measurement import Measurement, AgingStep
from .quality import QualityMetrics, QualityThreshold

__all__ = [
    'Spectrum',
    'SpectralData', 
    'Measurement',
    'AgingStep',
    'QualityMetrics',
    'QualityThreshold'
] 