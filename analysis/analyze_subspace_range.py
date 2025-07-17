#!/usr/bin/env python3
"""
Analyze subspace communication range for relay network planning
"""

import sys
sys.path.append(r'c:\Users\echo_\Code\asciimath\warp-field-coils\research')

from step17_subspace_transceiver import SubspaceTransceiver, SubspaceParams, TransmissionParams
import numpy as np

def analyze_transmission_range():
    """Analyze transmission range vs signal strength."""
    
    params = SubspaceParams(
        c_s=5e8,  # 1.67x speed of light  
        bandwidth=1e12,  # 1 THz bandwidth
        subspace_coupling=1e-15,  # Weak coupling
        loss_tangent=1e-6  # Low loss
    )
    
    transceiver = SubspaceTransceiver(params)
    
    # Test distances from Earth to various solar system boundaries
    distances = {
        "Earth orbit": 1.5e11,  # 1 AU
        "Mars orbit": 2.3e11,   # 1.5 AU
        "Jupiter orbit": 7.8e11, # 5.2 AU  
        "Saturn orbit": 1.4e12,  # 9.5 AU
        "Uranus orbit": 2.9e12,  # 19.2 AU
        "Neptune orbit": 4.5e12, # 30 AU
        "Kuiper Belt": 7.5e12,   # 50 AU
        "Heliopause": 1.8e13,    # 120 AU
        "Oort Cloud inner": 3.0e14, # 2000 AU
        "Oort Cloud outer": 1.5e16, # 100,000 AU
        "Proxima Centauri": 4.0e16, # 4.24 light years
    }
    
    print("=== SUBSPACE TRANSMISSION RANGE ANALYSIS ===")
    print(f"{'Location':<20} {'Distance (AU)':<15} {'Distance (ly)':<15} {'Signal (dB)':<12} {'Usable'}")
    print("-" * 75)
    
    results = {}
    
    for location, distance in distances.items():
        tx_params = TransmissionParams(
            frequency=2.4e12,  # 2.4 THz
            modulation_depth=0.8,
            duration=0.05,
            target_coordinates=(distance, 0, 0),
            priority=7
        )
        
        try:
            result = transceiver.transmit_message("Test", tx_params)
            signal_db = result['signal_strength_db']
            distance_au = distance / 1.5e11
            distance_ly = distance / 9.46e15
            usable = "YES" if signal_db > -60 else "NO"
            
            print(f"{location:<20} {distance_au:<15.1f} {distance_ly:<15.3f} {signal_db:<12.1f} {usable}")
            
            results[location] = {
                'distance_m': distance,
                'distance_au': distance_au, 
                'distance_ly': distance_ly,
                'signal_db': signal_db,
                'usable': signal_db > -60
            }
            
        except Exception as e:
            print(f"{location:<20} {distance/1.5e11:<15.1f} {distance/9.46e15:<15.3f} {'ERROR':<12} NO")
            results[location] = {'error': str(e)}
    
    return results

def calculate_relay_requirements():
    """Calculate relay network requirements for Earth-Proxima Centauri."""
    
    results = analyze_transmission_range()
    
    print("\n=== RELAY NETWORK CALCULATIONS ===")
    
    # Find maximum usable range
    max_range_m = 0
    max_range_location = ""
    
    for location, data in results.items():
        if 'usable' in data and data['usable'] and data['distance_m'] > max_range_m:
            max_range_m = data['distance_m']
            max_range_location = location
    
    proxima_distance = 4.0e16  # meters
    
    print(f"Maximum reliable transmission range: {max_range_location} ({max_range_m/1.5e11:.1f} AU)")
    print(f"Distance to Proxima Centauri: {proxima_distance/1.5e11:.0f} AU")
    
    if max_range_m > 0:
        num_relays = int(np.ceil(proxima_distance / max_range_m)) - 1
        print(f"Number of relay beacons required: {num_relays}")
        
        relay_spacing_au = (proxima_distance / (num_relays + 1)) / 1.5e11
        print(f"Relay spacing: {relay_spacing_au:.0f} AU")
        
        return num_relays, relay_spacing_au
    else:
        print("ERROR: No reliable transmission range found")
        return None, None

def calculate_earth_coverage():
    """Calculate Earth ground station requirements for 24/7 coverage."""
    
    print("\n=== EARTH GROUND STATION COVERAGE ===")
    
    # For 24/7 coverage of any direction in space, we need stations distributed
    # around Earth's surface. Minimum is 3 stations at 120° intervals.
    # For redundancy and better coverage during atmospheric interference,
    # recommend 6 stations at 60° intervals.
    
    min_stations = 3
    recommended_stations = 6
    
    print(f"Minimum ground stations for 24/7 coverage: {min_stations}")
    print(f"Recommended stations for redundancy: {recommended_stations}")
    
    # Station locations for optimal coverage
    station_locations = [
        ("North America", "40°N, 100°W", "Colorado, USA"),
        ("Europe/Africa", "45°N, 0°W", "France"),  
        ("Asia/Pacific", "35°N, 140°E", "Japan"),
        ("South America", "15°S, 60°W", "Brazil"),
        ("Australia", "25°S, 135°E", "Australia"),
        ("Antarctica", "75°S, 0°W", "Antarctica Base")
    ]
    
    print("\nRecommended ground station locations:")
    for i, (region, coords, location) in enumerate(station_locations, 1):
        print(f"  {i}. {region}: {coords} ({location})")
    
    print("\nTechnical requirements per station:")
    print("- Subspace transceiver array with 2.4 THz capability")
    print("- 360° azimuth, 0-90° elevation coverage")
    print("- Fiber optic connection to Internet backbone")
    print("- TCP/IP multiplexing capability")
    print("- Redundant power systems")
    print("- Atmospheric compensation systems")
    
    return recommended_stations, station_locations

if __name__ == "__main__":
    # Run analysis
    analyze_transmission_range()
    calculate_relay_requirements()
    calculate_earth_coverage()
