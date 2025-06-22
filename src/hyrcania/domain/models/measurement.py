"""
Measurement domain models for organizing spectroscopy data.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from .spectrum import Spectrum, SpectroscopyType


class AgingStep(Enum):
    """Aging steps for olive oil samples."""
    STEP_0 = 0
    STEP_1 = 1
    STEP_2 = 2
    STEP_3 = 3
    STEP_4 = 4
    STEP_5 = 5
    STEP_6 = 6
    STEP_7 = 7
    STEP_8 = 8
    STEP_9 = 9


@dataclass
class Measurement:
    """A complete measurement session with multiple spectra."""
    measurement_id: str
    aging_step: AgingStep
    spectroscopy_type: SpectroscopyType
    spectra: List[Spectrum]
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate measurement data."""
        if not self.spectra:
            raise ValueError("Measurement must contain at least one spectrum")
        
        # Ensure all spectra have the same spectroscopy type
        for spectrum in self.spectra:
            if spectrum.spectroscopy_type != self.spectroscopy_type:
                raise ValueError("All spectra must have the same spectroscopy type")
    
    @property
    def spectrum_count(self) -> int:
        """Get the number of spectra in this measurement."""
        return len(self.spectra)
    
    def get_spectrum_by_name(self, name: str) -> Optional[Spectrum]:
        """Get a spectrum by its measurement name."""
        for spectrum in self.spectra:
            if spectrum.measurement_name == name:
                return spectrum
        return None
    
    def get_spectra_by_excitation(self, excitation_wavelength: float) -> List[Spectrum]:
        """Get all spectra with a specific excitation wavelength."""
        return [
            spectrum for spectrum in self.spectra
            if spectrum.spectral_data.excitation_wavelength == excitation_wavelength
        ]
    
    def to_ramanspy_container(self):
        """Convert all spectra to a RamanSPy SpectralContainer."""
        import ramanspy as rp
        raman_spectra = [spectrum.to_ramanspy_spectrum() for spectrum in self.spectra]
        if raman_spectra:
            return rp.SpectralContainer(raman_spectra, spectral_axis=self.spectra[0].wavelengths)
        return None


@dataclass
class ExperimentSession:
    """A complete experiment session with multiple measurements."""
    session_id: str
    measurements: List[Measurement]
    experiment_config: Optional[Dict[str, Any]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def measurement_count(self) -> int:
        """Get the number of measurements in this session."""
        return len(self.measurements)
    
    def get_measurements_by_aging_step(self, aging_step: AgingStep) -> List[Measurement]:
        """Get all measurements for a specific aging step."""
        return [m for m in self.measurements if m.aging_step == aging_step]
    
    def get_measurements_by_type(self, spectroscopy_type: SpectroscopyType) -> List[Measurement]:
        """Get all measurements of a specific spectroscopy type."""
        return [m for m in self.measurements if m.spectroscopy_type == spectroscopy_type] 