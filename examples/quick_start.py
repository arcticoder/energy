#!/usr/bin/env python3
"""
Dynamic Backreaction Factor Framework - Quick Start Example
Basic usage demonstration for intelligent adaptive enhancement
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.dynamic_backreaction import DynamicBackreactionCalculator

def basic_usage_example():
    """Basic usage example for dynamic backreaction calculation"""
    print("🚀 Dynamic Backreaction Factor Framework - Quick Start")
    print("=" * 55)
    
    # Initialize the calculator
    calculator = DynamicBackreactionCalculator()
    print("✅ DynamicBackreactionCalculator initialized")
    
    # Example field conditions
    field_strength = 0.5  # Normalized field strength
    velocity = 0.2        # Field velocity component
    curvature = 0.1       # Local spacetime curvature
    
    print(f"\n📊 Input Parameters:")
    print(f"   Field Strength: {field_strength}")
    print(f"   Velocity: {velocity}")
    print(f"   Curvature: {curvature}")
    
    # Calculate dynamic enhancement factor
    beta_dynamic = calculator.calculate_dynamic_factor(
        field_strength=field_strength,
        velocity=velocity,
        curvature=curvature
    )
    
    # Compare with static factor
    beta_static = 1.9443254780147017
    improvement = ((beta_dynamic - beta_static) / beta_static) * 100
    
    print(f"\n🎯 Results:")
    print(f"   Static β: {beta_static:.6f}")
    print(f"   Dynamic β: {beta_dynamic:.6f}")
    print(f"   Improvement: {improvement:.2f}%")
    
    return beta_dynamic, improvement

def advanced_configuration_example():
    """Example with custom configuration parameters"""
    print("\n🔧 Advanced Configuration Example")
    print("-" * 35)
    
    # Custom configuration
    config = {
        'baseline_factor': 1.9443254780147017,
        'field_coupling': 0.15,    # Enhanced field coupling
        'velocity_coupling': 0.08,  # Increased velocity sensitivity
        'curvature_coupling': 0.03  # Enhanced curvature response
    }
    
    calculator = DynamicBackreactionCalculator(**config)
    print("✅ Custom configuration applied")
    
    # Test with various field conditions
    test_cases = [
        {'field_strength': 0.3, 'velocity': 0.1, 'curvature': 0.05, 'name': 'Low intensity'},
        {'field_strength': 0.7, 'velocity': 0.4, 'curvature': 0.15, 'name': 'Medium intensity'},
        {'field_strength': 1.0, 'velocity': 0.8, 'curvature': 0.25, 'name': 'High intensity'}
    ]
    
    print(f"\n📈 Testing various field conditions:")
    for case in test_cases:
        beta = calculator.calculate_dynamic_factor(
            field_strength=case['field_strength'],
            velocity=case['velocity'],
            curvature=case['curvature']
        )
        improvement = ((beta - config['baseline_factor']) / config['baseline_factor']) * 100
        print(f"   {case['name']:15} β = {beta:.6f} ({improvement:+.2f}%)")

def performance_benchmark_example():
    """Performance benchmarking example"""
    print("\n⚡ Performance Benchmark")
    print("-" * 25)
    
    import time
    import numpy as np
    
    calculator = DynamicBackreactionCalculator()
    
    # Generate test data
    n_calculations = 1000
    field_strengths = np.random.uniform(0.1, 1.0, n_calculations)
    velocities = np.random.uniform(0.05, 0.5, n_calculations)
    curvatures = np.random.uniform(0.01, 0.2, n_calculations)
    
    print(f"🔬 Performing {n_calculations} calculations...")
    
    start_time = time.perf_counter()
    
    results = []
    for i in range(n_calculations):
        beta = calculator.calculate_dynamic_factor(
            field_strength=field_strengths[i],
            velocity=velocities[i],
            curvature=curvatures[i]
        )
        results.append(beta)
    
    end_time = time.perf_counter()
    
    total_time = (end_time - start_time) * 1000  # Convert to milliseconds
    avg_time = total_time / n_calculations
    
    print(f"✅ Performance Results:")
    print(f"   Total time: {total_time:.2f} ms")
    print(f"   Average per calculation: {avg_time:.4f} ms")
    print(f"   Calculations per second: {1000/avg_time:.0f}")
    print(f"   Target: <1ms per calculation ✅" if avg_time < 1.0 else "   Target: <1ms per calculation ❌")

def main():
    """Main example function"""
    try:
        # Basic usage
        basic_usage_example()
        
        # Advanced configuration
        advanced_configuration_example()
        
        # Performance benchmark
        performance_benchmark_example()
        
        print("\n🎉 Quick Start Complete!")
        print("   Ready to deploy revolutionary adaptive enhancement technology!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Please ensure the framework is properly installed.")

if __name__ == "__main__":
    main()
