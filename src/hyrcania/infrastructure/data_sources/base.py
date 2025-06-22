"""
Base strategy interface for spectroscopy data loading.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pathlib import Path
import pandas as pd
import numpy as np

from hyrcania.domain.models.spectrum import Spectrum, SpectralData, SpectroscopyType
from hyrcania.domain.models.measurement import Measurement, AgingStep


class SpectroscopyStrategy(ABC):
    """Abstract base class for different spectroscopy data loading strategies."""
    
    def __init__(self, spectroscopy_type: SpectroscopyType):
        self.spectroscopy_type = spectroscopy_type
    
    @abstractmethod
    def load_data(self, file_path: Path) -> List[SpectralData]:
        """
        Load spectral data from a file.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            List of SpectralData objects
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from the file path or content.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Dictionary of metadata
        """
        pass
    
    @abstractmethod
    def validate_data(self, spectral_data: List[SpectralData]) -> bool:
        """
        Validate the loaded spectral data.
        
        Args:
            spectral_data: List of spectral data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def create_measurement(self, file_path: Path) -> Optional[Measurement]:
        """
        Create a Measurement object from a file.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Measurement object or None if failed
        """
        try:
            # Load spectral data
            spectral_data_list = self.load_data(file_path)
            
            if not self.validate_data(spectral_data_list):
                return None
            
            # Extract metadata
            metadata = self.extract_metadata(file_path)
            
            # Create spectra
            spectra = []
            for i, spectral_data in enumerate(spectral_data_list):
                spectrum = Spectrum(
                    spectral_data=spectral_data,
                    measurement_name=f"spectrum_{i}",
                    aging_step=self._extract_aging_step(file_path).value,
                    sample_id=self._extract_sample_id(file_path),
                    timestamp=metadata.get('timestamp')
                )
                spectra.append(spectrum)
            
            # Create measurement
            measurement = Measurement(
                measurement_id=file_path.stem,
                aging_step=self._extract_aging_step(file_path),
                spectroscopy_type=self.spectroscopy_type,
                spectra=spectra,
                metadata=metadata
            )
            
            return measurement
            
        except Exception as e:
            print(f"Error creating measurement from {file_path}: {e}")
            return None
    
    def _extract_aging_step(self, file_path: Path) -> AgingStep:
        """Extract aging step from file path."""
        filename = file_path.name
        if "AS0" in filename:
            return AgingStep.STEP_0
        elif "AS1" in filename:
            return AgingStep.STEP_1
        elif "AS2" in filename:
            return AgingStep.STEP_2
        elif "AS3" in filename:
            return AgingStep.STEP_3
        elif "AS4" in filename:
            return AgingStep.STEP_4
        elif "AS5" in filename:
            return AgingStep.STEP_5
        elif "AS6" in filename:
            return AgingStep.STEP_6
        elif "AS7" in filename:
            return AgingStep.STEP_7
        elif "AS8" in filename:
            return AgingStep.STEP_8
        elif "AS9" in filename:
            return AgingStep.STEP_9
        else:
            return AgingStep.STEP_0  # Default
    
    def _extract_sample_id(self, file_path: Path) -> str:
        """Extract sample ID from file path."""
        return file_path.stem 