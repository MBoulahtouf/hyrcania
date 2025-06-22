"""
Core spectrum domain models for spectroscopy data.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import numpy as np
from enum import Enum


class SpectroscopyType(Enum):
    """Types of spectroscopy measurements."""
    FLUORESCENCE = "fluorescence"
    ABSORPTION = "absorption"
    RAMAN = "raman"


@dataclass
class SpectralData:
    """Core spectral data structure with scientific metadata."""
    wavelengths: np.ndarray
    intensities: np.ndarray
    spectroscopy_type: SpectroscopyType
    excitation_wavelength: Optional[float] = None
    emission_wavelength: Optional[float] = None
    measurement_conditions: Optional[dict] = None
    
    def __post_init__(self):
        """Validate spectral data after initialization."""
        if len(self.wavelengths) != len(self.intensities):
            raise ValueError("Wavelengths and intensities must have the same length")
        
        if len(self.wavelengths) == 0:
            raise ValueError("Spectral data cannot be empty")
    
    @property
    def wavelength_range(self) -> Tuple[float, float]:
        """Get the wavelength range of the spectrum."""
        return float(self.wavelengths.min()), float(self.wavelengths.max())
    
    @property
    def intensity_range(self) -> Tuple[float, float]:
        """Get the intensity range of the spectrum."""
        return float(self.intensities.min()), float(self.intensities.max())
    
    @property
    def data_points(self) -> int:
        """Get the number of data points."""
        return len(self.wavelengths)
    
    def normalize(self, method: str = "minmax") -> 'SpectralData':
        """Normalize the spectral data."""
        if method == "minmax":
            normalized_intensities = (self.intensities - self.intensities.min()) / (self.intensities.max() - self.intensities.min())
        elif method == "zscore":
            normalized_intensities = (self.intensities - self.intensities.mean()) / self.intensities.std()
        else:
            raise ValueError(f"Unknown normalization method: {method}")
        
        return SpectralData(
            wavelengths=self.wavelengths,
            intensities=normalized_intensities,
            spectroscopy_type=self.spectroscopy_type,
            excitation_wavelength=self.excitation_wavelength,
            emission_wavelength=self.emission_wavelength,
            measurement_conditions=self.measurement_conditions
        )


@dataclass
class Spectrum:
    """A single spectrum measurement with metadata."""
    spectral_data: SpectralData
    measurement_name: str
    aging_step: Optional[int] = None
    sample_id: Optional[str] = None
    timestamp: Optional[str] = None
    
    @property
    def wavelengths(self) -> np.ndarray:
        return self.spectral_data.wavelengths
    
    @property
    def intensities(self) -> np.ndarray:
        return self.spectral_data.intensities
    
    @property
    def spectroscopy_type(self) -> SpectroscopyType:
        return self.spectral_data.spectroscopy_type
    
    def to_ramanspy_spectrum(self):
        """Convert to RamanSPy Spectrum object."""
        import ramanspy as rp
        return rp.Spectrum(self.intensities, self.wavelengths)
    
    def to_ramanspy_container(self):
        """Convert to RamanSPy SpectralContainer."""
        import ramanspy as rp
        spectrum = self.to_ramanspy_spectrum()
        return rp.SpectralContainer([spectrum], spectral_axis=self.wavelengths) 