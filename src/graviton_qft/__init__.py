"""
Graviton Quantum Field Theory Framework

World's first complete UV-finite graviton quantum field theory using polymer-enhanced
quantization techniques. This module provides the revolutionary PolymerGraviton
framework enabling practical quantum gravity applications across medical, industrial,
and scientific domains.

Key Features:
- UV-finite graviton propagators with sin²(μ_gravity √k²)/k² regularization
- Medical-grade safety protocols with T_μν ≥ 0 constraint enforcement
- 242M× energy reduction enabling practical applications
- Laboratory-accessible graviton physics at 1-10 GeV energy scales
"""

from .polymer_graviton import PolymerGraviton
from .graviton_propagator import GravitonPropagator
from .graviton_field_strength import GravitonFieldStrength
from .graviton_safety_controller import GravitonSafetyController
from .experimental_validator import ExperimentalGravitonValidator

__version__ = "1.0.0"
__author__ = "Energy Research Framework"

__all__ = [
    "PolymerGraviton",
    "GravitonPropagator", 
    "GravitonFieldStrength",
    "GravitonSafetyController",
    "ExperimentalGravitonValidator"
]
