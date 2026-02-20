"""
Machine Learning model for flood risk prediction
Combines satellite, weather, and elevation data
"""

import numpy as np
from datetime import datetime, timedelta
import pickle
import os


def load_model():
    """
    Load pre-trained flood prediction model
    In production: Load actual TensorFlow/PyTorch model
    """
    # Mock model for demo
    # In production: return tf.keras.models.load_model('models/flood_model.h5')
    return {'type': 'mock', 'version': '1.0'}


def predict_flood_risk(features, sensitivity='Medium'):
    """
    Predict flood risk using multi-modal data
    
    Args:
        features: Dict with satellite, weather, elevation, location data
        sensitivity: 'Low', 'Medium', or 'High' - affects threshold
    
    Returns:
        dict: Comprehensive risk assessment
    """
    # Extract features
    satellite_data = features.get('satellite')
    weather_data = features.get('weather')
    elevation_data = features.get('elevation')
    location = features.get('location')
    
    # Calculate individual risk scores
    risk_scores = {}
    
    # 1. Satellite risk (water coverage)
    if satellite_data:
        water_risk = calculate_satellite_risk(satellite_data)
        risk_scores['Satellite Analysis'] = water_risk
    
    # 2. Weather risk (rainfall)
    if weather_data:
        weather_risk = calculate_weather_risk(weather_data)
        risk_scores['Weather Forecast'] = weather_risk
    
    # 3. Elevation risk (topography)
    if elevation_data:
        terrain_risk = calculate_terrain_risk(elevation_data)
        risk_scores['Terrain Analysis'] = terrain_risk
    
    # 4. Historical risk (mock)
    historical_risk = calculate_historical_risk(location)
    risk_scores['Historical Data'] = historical_risk
    
    # Combine scores with weights
    weights = {
        'Satellite Analysis': 0.25,
        'Weather Forecast': 0.35,
        'Terrain Analysis': 0.25,
        'Historical Data': 0.15
    }
    
    overall_score = sum(risk_scores.get(k, 0) * weights[k] 
                       for k in weights.keys())
    
    # Adjust for sensitivity
    if sensitivity == 'High':
        overall_score *= 1.2
    elif sensitivity == 'Low':
        overall_score *= 0.8
    
    overall_score = min(100, max(0, overall_score))
    
    # Determine risk level
    if overall_score >= 70:
        risk_level = 'HIGH'
    elif overall_score >= 40:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    # Generate timeline forecast
    timeline = generate_risk_timeline(weather_data, overall_score)
    
    # Generate recommendations
    recommendations = generate_recommendations(risk_level, risk_scores)
    
    return {
        'score': round(overall_score, 1),
        'level': risk_level,
        'factors': risk_scores,
        'timeline': timeline,
        'recommendations': recommendations,
        'confidence': 0.85,  # Model confidence
        'updated': datetime.now()
    }


def calculate_satellite_risk(satellite_data):
    """Calculate risk from satellite imagery analysis"""
    # Mock calculation
    # In production: analyze NDWI, water body changes, etc.
    return np.random.uniform(20, 60)


def calculate_weather_risk(weather_data):
    """Calculate risk from weather forecast"""
    total_rainfall = sum(weather_data['rainfall_mm'])
    avg_humidity = weather_data['avg_humidity']
    
    # Risk increases with rainfall and humidity
    risk = 0
    
    if total_rainfall > 100:
        risk += 40
    elif total_rainfall > 50:
        risk += 25
    elif total_rainfall > 20:
        risk += 10
    
    if avg_humidity > 80:
        risk += 15
    elif avg_humidity > 70:
        risk += 8
    
    # Check for heavy rain in single day
    max_daily = max(weather_data['rainfall_mm'])
    if max_daily > 50:
        risk += 20
    elif max_daily > 30:
        risk += 10
    
    return min(100, risk)


def calculate_terrain_risk(elevation_data):
    """Calculate risk from elevation/topography"""
    center_elev = elevation_data['center_elevation']
    slope = elevation_data['slope']['average']
    
    risk = 0
    
    # Low elevation
    if center_elev < 50:
        risk += 35
    elif center_elev < 100:
        risk += 15
    
    # Flat terrain
    if slope < 2:
        risk += 30
    elif slope < 5:
        risk += 15
    
    return min(100, risk)


def calculate_historical_risk(location):
    """Calculate risk based on historical flood data"""
    # Mock historical analysis
    # In production: query historical flood database
    return np.random.uniform(10, 40)


def generate_risk_timeline(weather_data, base_risk):
    """Generate risk forecast for upcoming days"""
    if not weather_data:
        dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") 
                for i in range(3)]
        return {
            'dates': dates,
            'risk_scores': [base_risk] * 3
        }
    
    dates = weather_data['dates']
    rainfall = weather_data['rainfall_mm']
    
    # Risk increases with rainfall
    risk_scores = []
    for rain in rainfall:
        daily_risk = base_risk
        if rain > 30:
            daily_risk += 15
        elif rain > 15:
            daily_risk += 8
        risk_scores.append(min(100, daily_risk))
    
    return {
        'dates': dates,
        'risk_scores': risk_scores
    }


def generate_recommendations(risk_level, risk_factors):
    """Generate actionable recommendations based on risk"""
    recommendations = []
    
    if risk_level == 'HIGH':
        recommendations.append("⚠️ IMMEDIATE ACTION REQUIRED: Implement flood preparedness plan")
        recommendations.append("Monitor local authorities for evacuation orders")
        recommendations.append("Secure important documents and valuables on upper floors")
        recommendations.append("Prepare emergency supplies (water, food, first aid)")
        recommendations.append("Avoid unnecessary travel to affected areas")
    
    elif risk_level == 'MEDIUM':
        recommendations.append("Stay informed about weather updates")
        recommendations.append("Review your emergency evacuation plan")
        recommendations.append("Clear drainage systems around property")
        recommendations.append("Move vehicles to higher ground if possible")
        recommendations.append("Prepare sandbags if available")
    
    else:  # LOW
        recommendations.append("Continue normal activities with weather awareness")
        recommendations.append("Maintain clear drainage systems")
        recommendations.append("Keep emergency contact numbers updated")
    
    # Add specific recommendations based on factors
    for factor, score in risk_factors.items():
        if factor == 'Weather Forecast' and score > 50:
            recommendations.append("Heavy rainfall expected - monitor river levels")
        elif factor == 'Terrain Analysis' and score > 50:
            recommendations.append("Low-lying area - consider temporary relocation")
        elif factor == 'Satellite Analysis' and score > 50:
            recommendations.append("Increased water coverage detected - elevated risk")
    
    return recommendations


# PRODUCTION MODEL (commented out)
"""
import tensorflow as tf

def load_model_production():
    model = tf.keras.models.load_model('models/flood_model.h5')
    return model

def predict_flood_risk_production(features, model):
    # Prepare input tensor
    satellite_features = extract_cnn_features(features['satellite'])
    weather_features = normalize_weather(features['weather'])
    elevation_features = process_elevation(features['elevation'])
    
    # Combine features
    combined = tf.concat([
        satellite_features,
        weather_features,
        elevation_features
    ], axis=-1)
    
    # Predict
    prediction = model.predict(combined)
    risk_score = float(prediction[0][0] * 100)
    
    return risk_score
"""
