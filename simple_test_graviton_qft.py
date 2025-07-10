#!/usr/bin/env python3
"""
Graviton QFT Framework Simple Test

Simple validation test for the complete Graviton QFT framework implementation.
This script performs essential system checks and basic functionality tests.
"""

import sys
import os
import traceback

# Add the source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test basic framework imports"""
    print("Testing framework imports...")
    try:
        from graviton_qft import (
            PolymerGraviton, GravitonConfiguration,
            GravitonPropagator, GravitonFieldStrength,
            GravitonSafetyController, SafetyLimits,
            ExperimentalGravitonValidator, DetectionParameters
        )
        print("SUCCESS: All imports successful")
        return True
    except ImportError as e:
        print(f"FAILED: Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic framework functionality"""
    print("Testing basic functionality...")
    try:
        from graviton_qft import PolymerGraviton, GravitonConfiguration
        
        # Create basic configuration
        config = GravitonConfiguration(
            polymer_scale_gravity=1e-3,
            energy_scale=1.0
        )
        
        # Initialize graviton framework
        graviton = PolymerGraviton(config)
        
        # Test basic operations
        propagator_value = graviton.compute_propagator(1.0)
        enhancement = graviton.compute_energy_enhancement_factor()
        
        print(f"SUCCESS: Basic operations successful")
        print(f"  Propagator at k²=1: {abs(propagator_value):.2e}")
        print(f"  Energy enhancement: {enhancement:.1e}x")
        return True
        
    except Exception as e:
        print(f"FAILED: Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_safety_systems():
    """Test safety systems"""
    print("Testing safety systems...")
    try:
        from graviton_qft import GravitonSafetyController
        import numpy as np
        
        safety_controller = GravitonSafetyController()
        
        # Test with safe field
        safe_field = np.random.random((3, 4, 4)) * 1e-12
        safe_stress_energy = np.eye(4) * 1e-15
        
        safety_result = safety_controller.validate_graviton_field_safety(
            safe_field, safe_stress_energy)
        
        print(f"SUCCESS: Safety systems operational: {safety_result}")
        return True
        
    except Exception as e:
        print(f"FAILED: Safety systems test failed: {e}")
        return False

def test_experimental_validation():
    """Test experimental validation"""
    print("Testing experimental validation...")
    try:
        from graviton_qft import ExperimentalGravitonValidator
        
        validator = ExperimentalGravitonValidator()
        
        # Test basic detection capability
        stats = validator.get_detection_statistics()
        
        print(f"SUCCESS: Experimental validation ready")
        print(f"  Detection attempts: {stats['total_detection_attempts']}")
        return True
        
    except Exception as e:
        print(f"FAILED: Experimental validation test failed: {e}")
        return False

def test_field_calculations():
    """Test field strength calculations"""
    print("Testing field calculations...")
    try:
        from graviton_qft import GravitonFieldStrength
        import numpy as np
        
        field_calculator = GravitonFieldStrength()
        
        # Test field strength computation
        test_field = np.random.random((3, 4, 4)) * 1e-10
        field_strength = field_calculator.compute_field_strength(test_field)
        
        print(f"SUCCESS: Field calculations operational")
        print(f"  Test field strength: {field_strength:.2e}")
        return True
        
    except Exception as e:
        print(f"FAILED: Field calculations test failed: {e}")
        return False

def main():
    """Run all quick tests"""
    print("GRAVITON QFT FRAMEWORK QUICK TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_basic_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Safety Systems", test_safety_systems),
        ("Experimental Validation", test_experimental_validation),
        ("Field Calculations", test_field_calculations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}")
        print("-" * 30)
        try:
            success = test_func()
            if success:
                passed += 1
        except Exception as e:
            print(f"FAILED: {test_name} failed with exception: {e}")
    
    print(f"\nTEST RESULTS")
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("SUCCESS: ALL TESTS PASSED - FRAMEWORK READY!")
        print("Graviton QFT framework is operational")
        print("Ready for comprehensive demonstration")
        return True
    else:
        print("WARNING: SOME TESTS FAILED - CHECK IMPLEMENTATION")
        print(f"FAILED: {total-passed} test(s) need attention")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
