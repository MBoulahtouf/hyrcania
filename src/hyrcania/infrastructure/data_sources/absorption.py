"""
Absorption spectroscopy data loading strategy.
"""

from typing import List, Dict, Any, Tuple
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

from hyrcania.domain.models.spectrum import SpectralData, SpectroscopyType


class AbsorptionStrategy:
    """Strategy for loading absorption spectroscopy data."""
    
    def __init__(self):
        self.spectroscopy_type = SpectroscopyType.ABSORPTION
    
    def load_data(self, file_path: Path) -> List[SpectralData]:
        """
        Load absorption spectral data from a CSV file.
        
        Args:
            file_path: Path to the absorption CSV file
            
        Returns:
            List of SpectralData objects
        """
        try:
            df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
            spectral_data_list = []
            
            # Extract all wavelength-intensity pairs (every 2 columns)
            for i in range(0, df.shape[1] - 1, 2):
                try:
                    wavelengths, intensities = self._extract_spectrum(df, i)
                    if len(wavelengths) > 0:
                        spectral_data = SpectralData(
                            wavelengths=wavelengths,
                            intensities=intensities,
                            spectroscopy_type=SpectroscopyType.ABSORPTION
                        )
                        spectral_data_list.append(spectral_data)
                except Exception as e:
                    print(f"Error extracting spectrum from columns {i}-{i+1}: {e}")
                    continue
                    
            return spectral_data_list
            
        except Exception as e:
            print(f"Error loading absorption file {file_path}: {e}")
            return []
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from absorption file path."""
        return {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'spectroscopy_type': 'absorption',
            'timestamp': datetime.now().isoformat()
        }
    
    def validate_data(self, spectral_data: List[SpectralData]) -> bool:
        """Validate absorption spectral data."""
        if not spectral_data:
            return False
        
        for data in spectral_data:
            # Check wavelength range (UV-Vis typically 200-800 nm)
            if data.wavelength_range[0] < 100 or data.wavelength_range[1] > 1000:
                print(f"Warning: Wavelength range {data.wavelength_range} outside expected absorption range")
            
            # Check for negative absorbances
            if np.any(data.intensities < 0):
                print(f"Warning: Negative absorbances found in absorption data")
        
        return True
    
    def _extract_spectrum(self, df: pd.DataFrame, col_idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """Extract wavelength-intensity pair from dataframe columns."""
        if col_idx + 1 >= df.shape[1]:
            raise ValueError(f"Column index {col_idx} out of bounds")
        
        wavelength_col = df.iloc[:, col_idx]
        intensity_col = df.iloc[:, col_idx + 1]
        
        valid_mask = ~(wavelength_col.isna() | intensity_col.isna())
        wavelengths = wavelength_col[valid_mask].values.astype(float)
        intensities = intensity_col[valid_mask].values.astype(float)
        
        return wavelengths, intensities 