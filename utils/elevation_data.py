"""
Elevation/topography data using Open-Elevation API (free, unlimited)
No API key required!
"""

import requests
import numpy as np
from scipy.interpolate import griddata
import time


def get_elevation_profile(latitude, longitude, radius_km=5, resolution=20):
    """
    Get elevation profile for area around location
    
    Args:
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Radius in kilometers
        resolution: Number of points per side
    
    Returns:
        dict: Elevation data with risk analysis
    """
    try:
        # Create grid of points
        lat_offset = radius_km / 111  # Rough km to degrees
        lon_offset = radius_km / (111 * np.cos(np.radians(latitude)))
        
        lats = np.linspace(latitude - lat_offset, latitude + lat_offset, resolution)
        lons = np.linspace(longitude - lon_offset, longitude + lon_offset, resolution)
        
        # Prepare locations for API request
        locations = []
        for lat in lats:
            for lon in lons:
                locations.append({'latitude': lat, 'longitude': lon})
        
        # Call Open-Elevation API (free, no key needed!)
        url = 'https://api.open-elevation.com/api/v1/lookup'
        
        print(f"🌍 Fetching elevation data for {len(locations)} points...")
        
        # API can handle up to 100 locations per request
        # For larger grids, we'd need to batch
        if len(locations) > 100:
            # Reduce resolution for demo
            print("⚠️ Grid too large, using reduced resolution")
            resolution = 10
            lats = np.linspace(latitude - lat_offset, latitude + lat_offset, resolution)
            lons = np.linspace(longitude - lon_offset, longitude + lon_offset, resolution)
            locations = []
            for lat in lats:
                for lon in lons:
                    locations.append({'latitude': lat, 'longitude': lon})
        
        response = requests.post(
            url, 
            json={'locations': locations},
            timeout=30
        )
        
        if response.status_code == 200:
            results = response.json()['results']
            elevations = np.array([r['elevation'] for r in results])
            elevations = elevations.reshape(resolution, resolution)
            
            # Calculate center elevation
            center_idx = resolution // 2
            center_elevation = elevations[center_idx, center_idx]
            
            print(f"✅ Elevation data retrieved! Center elevation: {center_elevation}m")
            
            return {
                'latitudes': lats,
                'longitudes': lons,
                'elevations': elevations,
                'center_elevation': float(center_elevation),
                'min_elevation': float(np.min(elevations)),
                'max_elevation': float(np.max(elevations)),
                'avg_elevation': float(np.mean(elevations)),
                'slope': calculate_slope(elevations),
                'source': 'Open-Elevation API'
            }
        else:
            print(f"⚠️ Open-Elevation API error: {response.status_code}")
            return _get_mock_elevation_profile(latitude, longitude, radius_km, resolution)
            
    except requests.Timeout:
        print("⚠️ Elevation API timeout (server busy)")
        return _get_mock_elevation_profile(latitude, longitude, radius_km, resolution)
    
    except Exception as e:
        print(f"⚠️ Elevation API error: {str(e)}")
        return _get_mock_elevation_profile(latitude, longitude, radius_km, resolution)


def _get_mock_elevation_profile(latitude, longitude, radius_km=5, resolution=20):
    """Fallback mock data"""
    lat_offset = radius_km / 111
    lon_offset = radius_km / (111 * np.cos(np.radians(latitude)))
    
    lats = np.linspace(latitude - lat_offset, latitude + lat_offset, resolution)
    lons = np.linspace(longitude - lon_offset, longitude + lon_offset, resolution)
    
    # Mock elevation data
    elevations = []
    for lat in lats:
        row = []
        for lon in lons:
            elev = 100 + 50 * np.sin(lat * 10) + 30 * np.cos(lon * 10)
            elev += np.random.normal(0, 10)
            row.append(max(0, elev))
        elevations.append(row)
    
    elevations = np.array(elevations)
    
    return {
        'latitudes': lats,
        'longitudes': lons,
        'elevations': elevations,
        'center_elevation': float(elevations[resolution//2, resolution//2]),
        'min_elevation': float(np.min(elevations)),
        'max_elevation': float(np.max(elevations)),
        'avg_elevation': float(np.mean(elevations)),
        'slope': calculate_slope(elevations),
        'source': 'Mock Data'
    }


def calculate_slope(elevation_grid):
    """
    Calculate average terrain slope
    Higher slope = faster water runoff, lower flood risk
    Lower slope = water accumulation, higher flood risk
    """
    # Calculate gradient
    dy, dx = np.gradient(elevation_grid)
    slope = np.sqrt(dx**2 + dy**2)
    
    return {
        'average': float(np.mean(slope)),
        'max': float(np.max(slope)),
        'risk_factor': 'HIGH' if np.mean(slope) < 2 else 'MEDIUM' if np.mean(slope) < 5 else 'LOW'
    }


def calculate_flood_risk(elevation_data):
    """
    Calculate flood risk based on elevation and terrain
    
    Returns:
        dict: Terrain-based risk assessment
    """
    center_elev = elevation_data['center_elevation']
    avg_elev = elevation_data['avg_elevation']
    slope = elevation_data['slope']['average']
    
    # Risk factors
    risk_score = 0
    factors = []
    
    # Low elevation increases risk
    if center_elev < 50:
        risk_score += 30
        factors.append(f"Low elevation ({center_elev:.1f}m)")
    elif center_elev < 100:
        risk_score += 15
        factors.append(f"Moderate elevation ({center_elev:.1f}m)")
    
    # Below average elevation in area
    if center_elev < avg_elev - 20:
        risk_score += 25
        factors.append("Location is in a depression")
    
    # Low slope = water accumulation
    if slope < 2:
        risk_score += 25
        factors.append(f"Flat terrain (slope: {slope:.1f}°)")
    elif slope < 5:
        risk_score += 10
        factors.append(f"Gentle slope ({slope:.1f}°)")
    
    # Near sea level
    if center_elev < 10:
        risk_score += 20
        factors.append("Near sea level (coastal flood risk)")
    
    return {
        'risk_score': min(100, risk_score),
        'risk_level': 'HIGH' if risk_score > 50 else 'MEDIUM' if risk_score > 25 else 'LOW',
        'factors': factors,
        'terrain_type': classify_terrain(slope, center_elev),
        'source': elevation_data.get('source', 'Unknown')
    }


def classify_terrain(slope, elevation):
    """Classify terrain type"""
    if elevation < 10:
        return "Coastal Plain"
    elif slope < 2:
        return "Flat Lowland"
    elif slope < 5:
        return "Rolling Hills"
    elif slope < 10:
        return "Hilly Terrain"
    else:
        return "Mountainous"
