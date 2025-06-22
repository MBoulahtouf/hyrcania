"""
Fluorescence spectroscopy data loading strategy.
"""

from typing import List, Dict, Any, Tuple
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

from hyrcania.infrastructure.data_sources.base import SpectroscopyStrategy
from hyrcania.domain.models.spectrum import SpectralData, SpectroscopyType


class FluorescenceStrategy(SpectroscopyStrategy):
    """Strategy for loading fluorescence spectroscopy data."""
    
    def __init__(self):
        super().__init__(SpectroscopyType.FLUORESCENCE)
    
    def load_data(self, file_path: Path) -> List[SpectralData]:
        """
        Load fluorescence spectral data from a CSV file.
        
        Args:
            file_path: Path to the fluorescence CSV file
            
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
                            spectroscopy_type=SpectroscopyType.FLUORESCENCE,
                            excitation_wavelength=self._extract_excitation_wavelength(str(df.columns[i])),
                            emission_wavelength=None  # Will be calculated from wavelengths
                        )
                        spectral_data_list.append(spectral_data)
                except Exception as e:
                    print(f"Error extracting spectrum from columns {i}-{i+1}: {e}")
                    continue
                    
            return spectral_data_list
            
        except Exception as e:
            print(f"Error loading fluorescence file {file_path}: {e}")
            return []
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from fluorescence file path.
        
        Args:
            file_path: Path to the fluorescence file
            
        Returns:
            Dictionary of metadata
        """
        metadata = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'spectroscopy_type': 'fluorescence',
            'timestamp': datetime.now().isoformat(),
            'aging_step': self._extract_aging_step(file_path).value
        }
        
        # Extract additional metadata from filename
        filename = file_path.name
        if '_' in filename:
            parts = filename.split('_')
            if len(parts) >= 3:
                metadata['date'] = parts[0]
                metadata['time'] = parts[1]
                metadata['sample_code'] = parts[2]
        
        return metadata
    
    def validate_data(self, spectral_data: List[SpectralData]) -> bool:
        """
        Validate fluorescence spectral data.
        
        Args:
            spectral_data: List of spectral data to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not spectral_data:
            return False
        
        for data in spectral_data:
            # Check wavelength range (fluorescence typically 300-800 nm)
            if data.wavelength_range[0] < 200 or data.wavelength_range[1] > 1000:
                print(f"Warning: Wavelength range {data.wavelength_range} outside expected fluorescence range")
            
            # Check for negative intensities
            if np.any(data.intensities < 0):
                print(f"Warning: Negative intensities found in fluorescence data")
            
            # Check for NaN values
            if np.any(np.isnan(data.intensities)):
                print(f"Warning: NaN values found in fluorescence data")
        
        return True
    
    def _extract_spectrum(self, df: pd.DataFrame, col_idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract wavelength-intensity pair from dataframe columns.
        
        Args:
            df: DataFrame containing spectral data
            col_idx: Starting column index for wavelength column
            
        Returns:
            Tuple of (wavelengths, intensities)
        """
        if col_idx + 1 >= df.shape[1]:
            raise ValueError(f"Column index {col_idx} out of bounds")
        
        # Get wavelength and intensity columns
        wavelength_col = df.iloc[:, col_idx]
        intensity_col = df.iloc[:, col_idx + 1]
        
        # Remove rows with NaN values
        valid_mask = ~(wavelength_col.isna() | intensity_col.isna())
        wavelengths = wavelength_col[valid_mask].values.astype(float)
        intensities = intensity_col[valid_mask].values.astype(float)
        
        return wavelengths, intensities
    
    def _extract_excitation_wavelength(self, column_name: str) -> float:
        """
        Extract excitation wavelength from column name.
        
        Args:
            column_name: Name of the column
            
        Returns:
            Excitation wavelength in nm
        """
        try:
            # Example column name: "N0_EX_300.00"
            if 'EX_' in column_name:
                parts = column_name.split('EX_')
                if len(parts) > 1:
                    return float(parts[1])
        except (ValueError, IndexError):
            pass
        
        return 300.0  # Default excitation wavelength 