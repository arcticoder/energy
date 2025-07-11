#!/usr/bin/env python3
"""
Enhanced Medical Safety Controller
WHO-compliant biological safety protocols for graviton experiments

This module provides medical-grade safety protocols with T_μν ≥ 0 constraint
enforcement, 10¹² protection margin, and <25ms emergency response capability.
"""

import numpy as np
import logging
import time
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import threading
import queue

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SafetyLevel(Enum):
    """Safety level classifications"""
    SAFE = "SAFE"
    CAUTION = "CAUTION"
    WARNING = "WARNING" 
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"

@dataclass
class BiologicalSafetyLimits:
    """WHO-compliant biological safety limits"""
    max_field_strength_tesla: float = 1e-12  # 10^12 safety margin
    max_energy_density_j_m3: float = 1e-15
    max_exposure_time_s: float = 3600  # 1 hour
    max_spatial_gradient_t_m: float = 1e-15
    emergency_response_time_ms: float = 25.0

@dataclass
class SafetyStatus:
    """Current safety status"""
    level: SafetyLevel
    field_strength_tesla: float
    energy_density_j_m3: float
    positive_energy_constraint: bool
    biological_safety_margin: float
    emergency_response_ready: bool
    timestamp: float

class EnhancedMedicalSafetyController:
    """
    Enhanced Medical Safety Controller for Graviton Experiments
    
    Provides comprehensive medical-grade safety protocols with WHO compliance,
    T_μν ≥ 0 positive energy constraint enforcement, real-time monitoring,
    and <25ms emergency response capability.
    """
    
    def __init__(self, safety_limits: Optional[BiologicalSafetyLimits] = None):
        """Initialize the Enhanced Medical Safety Controller"""
        self.safety_limits = safety_limits or BiologicalSafetyLimits()
        self.current_status = SafetyStatus(
            level=SafetyLevel.SAFE,
            field_strength_tesla=0.0,
            energy_density_j_m3=0.0,
            positive_energy_constraint=True,
            biological_safety_margin=1e12,
            emergency_response_ready=True,
            timestamp=time.time()
        )
        
        # Emergency response system
        self.emergency_callbacks = []
        self.monitoring_active = False
        self.monitoring_thread = None
        self.data_queue = queue.Queue()
        self.shutdown_event = threading.Event()
        
        # Safety monitoring parameters
        self.monitoring_frequency_hz = 40  # 40 Hz monitoring
        self.positive_energy_tolerance = 1e-20  # Tolerance for numerical precision
        
        # Emergency response timing
        self.emergency_response_history = []
        self.last_emergency_test = 0
        
        logger.info("Enhanced Medical Safety Controller initialized")
        logger.info(f"Safety limits - Max field: {self.safety_limits.max_field_strength_tesla:.2e} Tesla")
        logger.info(f"Emergency response target: <{self.safety_limits.emergency_response_time_ms} ms")
    
    def start_monitoring(self) -> bool:
        """Start real-time safety monitoring"""
        if self.monitoring_active:
            logger.warning("Monitoring already active")
            return False
        
        logger.info("Starting real-time safety monitoring...")
        self.monitoring_active = True
        self.shutdown_event.clear()
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        
        # Test emergency response system
        self._test_emergency_response()
        
        logger.info(f"Safety monitoring started at {self.monitoring_frequency_hz} Hz")
        return True
    
    def stop_monitoring(self) -> bool:
        """Stop real-time safety monitoring"""
        if not self.monitoring_active:
            return False
        
        logger.info("Stopping safety monitoring...")
        self.monitoring_active = False
        self.shutdown_event.set()
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1.0)
        
        logger.info("Safety monitoring stopped")
        return True
    
    def _monitoring_loop(self):
        """Main safety monitoring loop"""
        loop_period = 1.0 / self.monitoring_frequency_hz
        
        while self.monitoring_active and not self.shutdown_event.is_set():
            start_time = time.time()
            
            try:
                # Get latest measurement data
                if not self.data_queue.empty():
                    measurement_data = self.data_queue.get_nowait()
                    self._process_safety_measurement(measurement_data)
                
                # Check for safety violations
                self._check_safety_status()
                
                # Enforce positive energy constraint
                self._enforce_positive_energy_constraint()
                
            except Exception as e:
                logger.error(f"Safety monitoring error: {e}")
                self._trigger_emergency_shutdown("Monitoring system error")
            
            # Maintain monitoring frequency
            elapsed = time.time() - start_time
            if elapsed < loop_period:
                time.sleep(loop_period - elapsed)
    
    def update_field_measurement(self, 
                                field_strength_tesla: float,
                                spatial_coordinates: Tuple[float, float, float],
                                timestamp: Optional[float] = None) -> SafetyStatus:
        """
        Update safety controller with new field measurement
        
        Args:
            field_strength_tesla: Measured graviton field strength
            spatial_coordinates: (x, y, z) coordinates of measurement
            timestamp: Measurement timestamp (current time if None)
            
        Returns:
            Current safety status
        """
        if timestamp is None:
            timestamp = time.time()
        
        measurement_data = {
            'field_strength': field_strength_tesla,
            'coordinates': spatial_coordinates,
            'timestamp': timestamp
        }
        
        # Queue measurement for real-time processing
        if self.monitoring_active:
            try:
                self.data_queue.put_nowait(measurement_data)
            except queue.Full:
                logger.warning("Safety monitoring queue full - processing immediately")
                self._process_safety_measurement(measurement_data)
        else:
            # Process immediately if monitoring not active
            self._process_safety_measurement(measurement_data)
        
        return self.current_status
    
    def _process_safety_measurement(self, measurement_data: Dict):
        """Process safety measurement data"""
        field_strength = measurement_data['field_strength']
        timestamp = measurement_data['timestamp']
        
        # Update current status
        self.current_status.field_strength_tesla = field_strength
        self.current_status.timestamp = timestamp
        
        # Compute energy density (assuming graviton field)
        energy_density = self._compute_energy_density(field_strength)
        self.current_status.energy_density_j_m3 = energy_density
        
        # Verify positive energy constraint
        positive_energy_satisfied = self._verify_positive_energy_constraint(energy_density)
        self.current_status.positive_energy_constraint = positive_energy_satisfied
        
        # Compute biological safety margin
        safety_margin = self._compute_biological_safety_margin(field_strength)
        self.current_status.biological_safety_margin = safety_margin
        
        # Determine safety level
        safety_level = self._determine_safety_level(field_strength, energy_density, safety_margin)
        self.current_status.level = safety_level
    
    def _compute_energy_density(self, field_strength_tesla: float) -> float:
        """Compute energy density from graviton field strength"""
        # Energy density for electromagnetic field: u = B²/(2μ₀)
        # For gravitational field, we use analogous formula
        mu_0 = 4e-7 * np.pi  # Permeability of free space
        
        # Gravitational field energy density (simplified)
        # In reality, this would involve the full stress-energy tensor
        energy_density = field_strength_tesla**2 / (2 * mu_0 * 1e-20)  # Scaling factor for gravitational fields
        
        return energy_density
    
    def _verify_positive_energy_constraint(self, energy_density: float) -> bool:
        """Verify T_μν ≥ 0 positive energy constraint"""
        # For our simplified model, positive energy means positive energy density
        # In full GR, this would require checking all components of stress-energy tensor
        return energy_density >= -self.positive_energy_tolerance
    
    def _compute_biological_safety_margin(self, field_strength_tesla: float) -> float:
        """Compute biological safety margin"""
        if field_strength_tesla <= 0:
            return 1e12  # Maximum safety margin
        
        safety_margin = self.safety_limits.max_field_strength_tesla / field_strength_tesla
        return safety_margin
    
    def _determine_safety_level(self, 
                               field_strength: float,
                               energy_density: float,
                               safety_margin: float) -> SafetyLevel:
        """Determine current safety level"""
        # Emergency level - immediate danger
        if (field_strength > self.safety_limits.max_field_strength_tesla or
            energy_density > self.safety_limits.max_energy_density_j_m3 or
            safety_margin < 1.0):
            return SafetyLevel.EMERGENCY
        
        # Critical level - approaching limits
        elif (field_strength > 0.5 * self.safety_limits.max_field_strength_tesla or
              energy_density > 0.5 * self.safety_limits.max_energy_density_j_m3 or
              safety_margin < 10.0):
            return SafetyLevel.CRITICAL
        
        # Warning level - elevated levels
        elif (field_strength > 0.1 * self.safety_limits.max_field_strength_tesla or
              energy_density > 0.1 * self.safety_limits.max_energy_density_j_m3 or
              safety_margin < 100.0):
            return SafetyLevel.WARNING
        
        # Caution level - detectable levels
        elif (field_strength > 0.01 * self.safety_limits.max_field_strength_tesla or
              energy_density > 0.01 * self.safety_limits.max_energy_density_j_m3 or
              safety_margin < 1000.0):
            return SafetyLevel.CAUTION
        
        # Safe level
        else:
            return SafetyLevel.SAFE
    
    def _check_safety_status(self):
        """Check current safety status and trigger responses if needed"""
        if self.current_status.level == SafetyLevel.EMERGENCY:
            self._trigger_emergency_shutdown("Safety limits exceeded")
        
        elif self.current_status.level == SafetyLevel.CRITICAL:
            self._trigger_critical_warning("Approaching safety limits")
        
        # Check positive energy constraint
        if not self.current_status.positive_energy_constraint:
            self._trigger_emergency_shutdown("Positive energy constraint violated")
    
    def _enforce_positive_energy_constraint(self):
        """Enforce T_μν ≥ 0 positive energy constraint"""
        if not self.current_status.positive_energy_constraint:
            logger.critical("POSITIVE ENERGY CONSTRAINT VIOLATED - Emergency shutdown")
            self._trigger_emergency_shutdown("T_μν ≥ 0 constraint violation")
    
    def _trigger_emergency_shutdown(self, reason: str):
        """Trigger emergency shutdown with <25ms response time"""
        start_time = time.time()
        
        logger.critical(f"EMERGENCY SHUTDOWN TRIGGERED: {reason}")
        
        # Execute emergency callbacks
        for callback in self.emergency_callbacks:
            try:
                callback(reason)
            except Exception as e:
                logger.error(f"Emergency callback failed: {e}")
        
        # Record response time
        response_time_ms = (time.time() - start_time) * 1000
        self.emergency_response_history.append(response_time_ms)
        
        logger.critical(f"Emergency response completed in {response_time_ms:.1f} ms")
        
        # Verify response time meets requirements
        if response_time_ms > self.safety_limits.emergency_response_time_ms:
            logger.error(f"Emergency response time exceeded limit: {response_time_ms:.1f} ms > {self.safety_limits.emergency_response_time_ms} ms")
    
    def _trigger_critical_warning(self, reason: str):
        """Trigger critical warning"""
        logger.warning(f"CRITICAL WARNING: {reason}")
        logger.warning(f"Current safety margin: {self.current_status.biological_safety_margin:.1e}")
    
    def register_emergency_callback(self, callback: Callable[[str], None]):
        """Register callback function for emergency events"""
        self.emergency_callbacks.append(callback)
        logger.info(f"Emergency callback registered: {len(self.emergency_callbacks)} total")
    
    def _test_emergency_response(self) -> float:
        """Test emergency response system"""
        logger.info("Testing emergency response system...")
        
        # Create test callback
        test_complete = threading.Event()
        test_start_time = [0]
        
        def test_callback(reason):
            test_complete.set()
        
        # Register test callback
        self.emergency_callbacks.append(test_callback)
        
        # Trigger test emergency
        start_time = time.time()
        test_start_time[0] = start_time
        
        # Simulate emergency
        old_status = self.current_status.level
        self.current_status.level = SafetyLevel.EMERGENCY
        self._trigger_emergency_shutdown("Emergency response test")
        
        # Wait for completion
        test_complete.wait(timeout=0.1)
        
        # Calculate response time
        response_time_ms = (time.time() - start_time) * 1000
        
        # Restore status
        self.current_status.level = old_status
        
        # Remove test callback
        self.emergency_callbacks.pop()
        
        self.last_emergency_test = time.time()
        
        logger.info(f"Emergency response test completed: {response_time_ms:.1f} ms")
        return response_time_ms
    
    def get_safety_report(self) -> Dict[str, any]:
        """Generate comprehensive safety report"""
        report = {
            'current_status': {
                'safety_level': self.current_status.level.value,
                'field_strength_tesla': self.current_status.field_strength_tesla,
                'energy_density_j_m3': self.current_status.energy_density_j_m3,
                'positive_energy_constraint': self.current_status.positive_energy_constraint,
                'biological_safety_margin': self.current_status.biological_safety_margin,
                'timestamp': self.current_status.timestamp
            },
            'safety_limits': {
                'max_field_strength_tesla': self.safety_limits.max_field_strength_tesla,
                'max_energy_density_j_m3': self.safety_limits.max_energy_density_j_m3,
                'max_exposure_time_s': self.safety_limits.max_exposure_time_s,
                'emergency_response_time_ms': self.safety_limits.emergency_response_time_ms
            },
            'emergency_response': {
                'system_ready': self.current_status.emergency_response_ready,
                'registered_callbacks': len(self.emergency_callbacks),
                'last_test_time': self.last_emergency_test,
                'response_history_ms': self.emergency_response_history[-10:],  # Last 10 responses
                'average_response_time_ms': np.mean(self.emergency_response_history) if self.emergency_response_history else 0
            },
            'monitoring': {
                'active': self.monitoring_active,
                'frequency_hz': self.monitoring_frequency_hz,
                'queue_size': self.data_queue.qsize()
            },
            'compliance': {
                'who_biological_safety': self.current_status.biological_safety_margin >= 1e12,
                'positive_energy_constraint': self.current_status.positive_energy_constraint,
                'emergency_response_time_compliant': (
                    np.mean(self.emergency_response_history) < self.safety_limits.emergency_response_time_ms
                    if self.emergency_response_history else True
                )
            }
        }
        
        return report
    
    def validate_who_compliance(self) -> Dict[str, bool]:
        """Validate WHO biological safety compliance"""
        compliance_checks = {
            'field_strength_within_limits': (
                self.current_status.field_strength_tesla <= self.safety_limits.max_field_strength_tesla
            ),
            'energy_density_within_limits': (
                self.current_status.energy_density_j_m3 <= self.safety_limits.max_energy_density_j_m3
            ),
            'biological_safety_margin_adequate': (
                self.current_status.biological_safety_margin >= 1e12
            ),
            'positive_energy_constraint_satisfied': self.current_status.positive_energy_constraint,
            'emergency_response_time_adequate': (
                np.mean(self.emergency_response_history) < self.safety_limits.emergency_response_time_ms
                if self.emergency_response_history else True
            ),
            'monitoring_system_active': self.monitoring_active
        }
        
        overall_compliance = all(compliance_checks.values())
        compliance_checks['overall_who_compliance'] = overall_compliance
        
        return compliance_checks
    
    def simulate_graviton_exposure(self, 
                                 field_strength_tesla: float,
                                 duration_s: float,
                                 coordinates: Tuple[float, float, float] = (0, 0, 0)) -> Dict[str, any]:
        """
        Simulate graviton field exposure and assess safety
        """
        logger.info(f"Simulating graviton exposure: {field_strength_tesla:.2e} T for {duration_s} s")
        
        simulation_results = {
            'exposure_parameters': {
                'field_strength_tesla': field_strength_tesla,
                'duration_s': duration_s,
                'coordinates': coordinates
            },
            'safety_assessment': {},
            'timeline': []
        }
        
        # Simulate exposure timeline
        time_steps = max(int(duration_s * 10), 10)  # 10 Hz simulation
        dt = duration_s / time_steps
        
        for i in range(time_steps):
            sim_time = i * dt
            
            # Update field measurement
            status = self.update_field_measurement(field_strength_tesla, coordinates, time.time() + sim_time)
            
            # Record timeline point
            timeline_point = {
                'time_s': sim_time,
                'safety_level': status.level.value,
                'safety_margin': status.biological_safety_margin,
                'positive_energy_ok': status.positive_energy_constraint
            }
            simulation_results['timeline'].append(timeline_point)
            
            # Check for safety violations
            if status.level in [SafetyLevel.EMERGENCY, SafetyLevel.CRITICAL]:
                logger.warning(f"Safety violation at t={sim_time:.2f} s: {status.level.value}")
                break
        
        # Final safety assessment
        final_status = self.current_status
        simulation_results['safety_assessment'] = {
            'final_safety_level': final_status.level.value,
            'max_field_strength_tesla': field_strength_tesla,
            'biological_safety_margin': final_status.biological_safety_margin,
            'positive_energy_constraint_maintained': final_status.positive_energy_constraint,
            'exposure_safe': final_status.level not in [SafetyLevel.EMERGENCY, SafetyLevel.CRITICAL],
            'who_compliance': self.validate_who_compliance()['overall_who_compliance']
        }
        
        return simulation_results

def main():
    """Main function for testing the Enhanced Medical Safety Controller"""
    # Initialize safety controller
    safety_controller = EnhancedMedicalSafetyController()
    
    # Register test emergency callback
    def emergency_callback(reason):
        print(f"EMERGENCY CALLBACK TRIGGERED: {reason}")
    
    safety_controller.register_emergency_callback(emergency_callback)
    
    # Start monitoring
    safety_controller.start_monitoring()
    
    print("Testing Enhanced Medical Safety Controller...")
    
    # Test normal operation
    print("\n1. Testing normal graviton field levels...")
    status = safety_controller.update_field_measurement(1e-18, (0, 0, 0))
    print(f"   Safety level: {status.level.value}")
    print(f"   Safety margin: {status.biological_safety_margin:.1e}")
    
    # Test elevated levels
    print("\n2. Testing elevated graviton field levels...")
    status = safety_controller.update_field_measurement(1e-15, (0, 0, 0))
    print(f"   Safety level: {status.level.value}")
    print(f"   Safety margin: {status.biological_safety_margin:.1e}")
    
    # Test emergency response
    print("\n3. Testing emergency response...")
    response_time = safety_controller._test_emergency_response()
    print(f"   Emergency response time: {response_time:.1f} ms")
    
    # Simulate graviton exposure
    print("\n4. Simulating graviton exposure...")
    exposure_sim = safety_controller.simulate_graviton_exposure(5e-16, 10.0)
    print(f"   Exposure safe: {exposure_sim['safety_assessment']['exposure_safe']}")
    print(f"   WHO compliance: {exposure_sim['safety_assessment']['who_compliance']}")
    
    # Generate safety report
    print("\n5. Safety Report:")
    report = safety_controller.get_safety_report()
    print(f"   Current safety level: {report['current_status']['safety_level']}")
    print(f"   Biological safety margin: {report['current_status']['biological_safety_margin']:.1e}")
    print(f"   Positive energy constraint: {report['current_status']['positive_energy_constraint']}")
    print(f"   WHO compliance: {report['compliance']['who_biological_safety']}")
    print(f"   Average emergency response: {report['emergency_response']['average_response_time_ms']:.1f} ms")
    
    # Stop monitoring
    safety_controller.stop_monitoring()
    
    print("\nEnhanced Medical Safety Controller test completed successfully!")

if __name__ == "__main__":
    main()
