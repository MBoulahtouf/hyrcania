#!/usr/bin/env python3
"""
Test script to demonstrate the refactored Hyrcania architecture.
Shows the new design patterns in action.
"""

import sys
from pathlib import Path
import numpy as np

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_domain_models():
    """Test the new domain models."""
    print("🧪 Testing Domain Models")
    print("=" * 50)
    
    try:
        from hyrcania.domain.models.spectrum import SpectralData, SpectroscopyType, Spectrum
        from hyrcania.domain.models.measurement import Measurement, AgingStep
        from hyrcania.domain.models.quality import QualityMetrics, QualityGrade
        
        # Test SpectralData
        wavelengths = np.linspace(300, 800, 251)
        intensities = np.random.random(251)
        
        spectral_data = SpectralData(
            wavelengths=wavelengths,
            intensities=intensities,
            spectroscopy_type=SpectroscopyType.FLUORESCENCE,
            excitation_wavelength=300.0
        )
        
        print(f"✅ Created SpectralData:")
        print(f"   Wavelength range: {spectral_data.wavelength_range}")
        print(f"   Intensity range: {spectral_data.intensity_range}")
        print(f"   Data points: {spectral_data.data_points}")
        
        # Test Spectrum
        spectrum = Spectrum(
            spectral_data=spectral_data,
            measurement_name="test_spectrum",
            aging_step=0,
            sample_id="test_sample"
        )
        
        print(f"✅ Created Spectrum:")
        print(f"   Measurement name: {spectrum.measurement_name}")
        print(f"   Aging step: {spectrum.aging_step}")
        
        # Test QualityMetrics
        quality_metrics = QualityMetrics(
            acidity=0.5,
            peroxide_value=15.0,
            k232=2.0,
            k270=0.15
        )
        
        overall_score = quality_metrics.calculate_overall_score()
        quality_grade = quality_metrics.determine_quality_grade()
        
        print(f"✅ Created QualityMetrics:")
        print(f"   Overall score: {overall_score:.2f}")
        print(f"   Quality grade: {quality_grade.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain models test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_strategy_pattern():
    """Test the strategy pattern for data loading."""
    print("\n🧪 Testing Strategy Pattern")
    print("=" * 50)
    
    try:
        from hyrcania.infrastructure.data_sources.fluorescence import FluorescenceStrategy
        from hyrcania.infrastructure.data_sources.absorption import AbsorptionStrategy
        
        # Test fluorescence strategy
        fluorescence_strategy = FluorescenceStrategy()
        print(f"✅ Created FluorescenceStrategy: {fluorescence_strategy.spectroscopy_type.value}")
        
        # Test absorption strategy
        absorption_strategy = AbsorptionStrategy()
        print(f"✅ Created AbsorptionStrategy: {absorption_strategy.spectroscopy_type.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Strategy pattern test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_factory_pattern():
    """Test the factory pattern."""
    print("\n🧪 Testing Factory Pattern")
    print("=" * 50)
    
    try:
        from hyrcania.infrastructure.data_sources.factory import SpectroscopyDataSourceFactory
        from hyrcania.domain.models.spectrum import SpectroscopyType
        
        # Test factory creation
        fluorescence_strategy = SpectroscopyDataSourceFactory.create_strategy(SpectroscopyType.FLUORESCENCE)
        print(f"✅ Factory created FluorescenceStrategy: {fluorescence_strategy.spectroscopy_type.value}")
        
        absorption_strategy = SpectroscopyDataSourceFactory.create_strategy(SpectroscopyType.ABSORPTION)
        print(f"✅ Factory created AbsorptionStrategy: {absorption_strategy.spectroscopy_type.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Factory pattern test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_loading():
    """Test data loading with the new architecture."""
    print("\n🧪 Testing Data Loading")
    print("=" * 50)
    
    try:
        from hyrcania.infrastructure.data_sources.factory import SpectroscopyDataSourceFactory
        from hyrcania.domain.models.spectrum import SpectroscopyType
        
        # Find a fluorescence file
        data_dir = Path("data/extracted")
        fluorescence_files = list(data_dir.rglob("**/Fluorescence/*.csv"))
        
        if not fluorescence_files:
            print("❌ No fluorescence files found")
            return False
        
        test_file = fluorescence_files[0]
        print(f"📁 Testing with file: {test_file.name}")
        
        # Create strategy and load data
        strategy = SpectroscopyDataSourceFactory.create_strategy(SpectroscopyType.FLUORESCENCE)
        spectral_data_list = strategy.load_data(test_file)
        
        print(f"✅ Loaded {len(spectral_data_list)} spectral data objects")
        
        if spectral_data_list:
            first_data = spectral_data_list[0]
            print(f"   First spectrum: {first_data.wavelength_range} nm, {first_data.data_points} points")
        
        return True
        
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 Testing Refactored Hyrcania Architecture")
    print("=" * 60)
    
    tests = [
        ("Domain Models", test_domain_models),
        ("Strategy Pattern", test_strategy_pattern),
        ("Factory Pattern", test_factory_pattern),
        ("Data Loading", test_data_loading),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! The refactored architecture is working.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main() 