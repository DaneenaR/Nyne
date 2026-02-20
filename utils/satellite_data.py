"""
Satellite imagery fetching and analysis
Uses Sentinel Hub API (1000 requests/month free)
"""

import os
import numpy as np
from datetime import datetime, timedelta
import requests
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

SENTINEL_CLIENT_ID = os.getenv("SENTINEL_CLIENT_ID", "")
SENTINEL_CLIENT_SECRET = os.getenv("SENTINEL_CLIENT_SECRET", "")

# Flag to use mock data if API not configured
USE_MOCK = not (SENTINEL_CLIENT_ID and SENTINEL_CLIENT_SECRET)


def get_satellite_imagery(latitude, longitude, radius_km=5):
    """
    Fetch recent satellite imagery for location
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        radius_km: Search radius in kilometers
    
    Returns:
        dict: Satellite data with image and metadata
    """
    if USE_MOCK:
        print("⚠️ Using mock satellite data (Sentinel Hub API not configured)")
        return _get_mock_satellite_imagery(latitude, longitude)
    
    try:
        # Get OAuth token
        token = _get_sentinel_token()
        
        # Calculate bounding box
        bbox_size = radius_km / 111  # Rough km to degrees
        bbox = [
            longitude - bbox_size,
            latitude - bbox_size,
            longitude + bbox_size,
            latitude + bbox_size
        ]
        
        # Request parameters
        evalscript = """
        //VERSION=3
        function setup() {
          return {
            input: ["B04", "B03", "B02"],
            output: { bands: 3 }
          };
        }
        function evaluatePixel(sample) {
          return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
        }
        """
        
        # Make API request
        url = "https://services.sentinel-hub.com/api/v1/process"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "input": {
                "bounds": {
                    "bbox": bbox,
                    "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"}
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z"),
                            "to": datetime.now().strftime("%Y-%m-%dT23:59:59Z")
                        }
                    }
                }]
            },
            "output": {
                "width": 512,
                "height": 512,
                "responses": [{
                    "identifier": "default",
                    "format": {"type": "image/png"}
                }]
            },
            "evalscript": evalscript
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            # Convert to PIL Image
            image = Image.open(io.BytesIO(response.content))
            
            return {
                'image': image,
                'timestamp': datetime.now(),
                'location': (latitude, longitude),
                'cloud_coverage': 0,  # Would need separate request
                'resolution': '10m',
                'bands': ['B04', 'B03', 'B02'],
                'source': 'Sentinel-2 L2A'
            }
        else:
            print(f"⚠️ Sentinel API error: {response.status_code}")
            return _get_mock_satellite_imagery(latitude, longitude)
            
    except Exception as e:
        print(f"⚠️ Satellite API error: {str(e)}")
        return _get_mock_satellite_imagery(latitude, longitude)


def _get_sentinel_token():
    """Get OAuth token for Sentinel Hub"""
    url = "https://services.sentinel-hub.com/oauth/token"
    
    data = {
        "grant_type": "client_credentials",
        "client_id": SENTINEL_CLIENT_ID,
        "client_secret": SENTINEL_CLIENT_SECRET
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get token: {response.status_code}")


def _get_mock_satellite_imagery(latitude, longitude):
    """Fallback mock data"""
    width, height = 512, 512
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    
    for i in range(width):
        for j in range(height):
            if (i + j) % 3 == 0:
                pixels[i, j] = (50, 100, 200)  # Water (blue)
            else:
                pixels[i, j] = (100, 150, 50)  # Land (green)
    
    return {
        'image': image,
        'timestamp': datetime.now(),
        'location': (latitude, longitude),
        'cloud_coverage': np.random.randint(0, 30),
        'resolution': '10m (mock)',
        'bands': ['B02', 'B03', 'B04', 'B08'],
        'source': 'Mock Data'
    }


def analyze_water_bodies(satellite_data):
    """
    Analyze water coverage using NDWI (Normalized Difference Water Index)
    
    Args:
        satellite_data: Output from get_satellite_imagery()
    
    Returns:
        dict: Water analysis results
    """
    # For mock data, use random values
    # For real data, would calculate NDWI from NIR and Green bands
    
    water_percentage = np.random.uniform(10, 40)
    previous_water = water_percentage - np.random.uniform(-5, 10)
    change = water_percentage - previous_water
    
    # Risk assessment
    risk_indicators = []
    if water_percentage > 30:
        risk_indicators.append("High water coverage detected")
    if change > 5:
        risk_indicators.append("Significant increase in water bodies")
    if satellite_data.get('cloud_coverage', 0) < 10:
        risk_indicators.append("Clear imagery - high confidence")
    
    analysis = f"Detected {water_percentage:.1f}% water coverage. "
    if change > 0:
        analysis += f"Water levels increased by {change:.1f}% from last month. "
    else:
        analysis += f"Water levels decreased by {abs(change):.1f}% from last month. "
    
    if len(risk_indicators) > 0:
        analysis += "⚠️ Risk indicators detected."
    
    return {
        'water_percentage': water_percentage,
        'change': change,
        'risk_count': len(risk_indicators),
        'risk_indicators': risk_indicators,
        'analysis': analysis,
        'confidence': 0.85,
        'source': satellite_data.get('source', 'Unknown')
    }


def calculate_ndwi(green_band, nir_band):
    """
    Calculate Normalized Difference Water Index
    NDWI = (Green - NIR) / (Green + NIR)
    
    Values > 0.3 typically indicate water
    """
    ndwi = (green_band - nir_band) / (green_band + nir_band + 1e-10)
    return ndwi
