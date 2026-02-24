## Nyne Flood Detection System

**Multi-modal AI system for real-time flood risk prediction and early warning**
## Features

### **Satellite Analysis**
- Real-time satellite imagery from Sentinel Hub
- Water body detection using NDWI (Normalized Difference Water Index)
- Land cover change detection
- Cloud coverage assessment

### **Weather Integration**
- Live weather forecasts (7-day)
- Rainfall predictions and tracking
- Temperature and humidity monitoring
- Storm alert integration

### **Terrain Analysis**
- Elevation profile mapping
- Slope calculation for runoff assessment
- Low-lying area identification
- Coastal flood risk evaluation

### **AI Prediction Model**
- Multi-modal deep learning
- Real-time risk scoring (0-100%)
- Timeline forecasting
- Confidence intervals

### **Interactive Dashboard**
- Real-time risk maps
- Risk factor breakdown
- Historical trends
- Actionable recommendations

### Prerequisites
- Python 3.8+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/flood-detection.git
cd flood-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


```

### Get Free API Keys

**1. Sentinel Hub (Satellite Imagery)**
- Sign up: https://www.sentinel-hub.com/
- Get 1000 requests/month free
- Copy Client ID and Secret to `.env`

**2. OpenWeatherMap (Weather Data)**
- Sign up: https://openweathermap.org/api
- Free tier: 1000 calls/day
- Copy API key to `.env`

**3. Open-Elevation (No key needed!)**
- Unlimited free usage
- No sign-up required

### Run the App

```bash
# Start Streamlit dashboard
streamlit run app.py
```

Open http://localhost:8501 in your browser

## How It Works

### 1. **Data Collection**
```
User Input (Location)
    ↓
┌──────────────┬──────────────┬──────────────┐
│   Satellite  │   Weather    │  Elevation   │
│   Imagery    │   Forecast   │     Data     │
└──────────────┴──────────────┴──────────────┘
```

### 2. **Feature Extraction**
- **Satellite:** NDWI, water coverage %, change detection
- **Weather:** Rainfall (mm), humidity (%), temperature (°C)
- **Elevation:** Slope (degrees), depression areas, sea level

### 3. **AI Prediction**
```python
Risk Score = (
    0.25 × Satellite_Risk +
    0.35 × Weather_Risk +
    0.25 × Terrain_Risk +
    0.15 × Historical_Risk
)
```

### 4. **Risk Classification**
- **HIGH (70-100%):** Immediate action required
- **MEDIUM (40-69%):** Elevated risk, prepare
- **LOW (0-39%):** Normal monitoring

## Project Structure
```
flood-detection/
├── app.py                          # Main Streamlit dashboard
├── requirements.txt                # Dependencies
├── .env.example                    # Environment template
├── README.md                       # This file
├── utils/
│   ├── __init__.py
│   ├── satellite_data.py          # Sentinel Hub integration
│   ├── weather_data.py            # Weather API integration
│   ├── elevation_data.py          # Elevation analysis
│   └── ml_model.py                # Prediction model
├── models/
│   └── flood_model.h5             # Pre-trained model (optional)
├── data/
│   ├── satellite/                 # Cached satellite images
│   ├── weather/                   # Weather data cache
│   └── processed/                 # Processed datasets
├── notebooks/
│   └── model_training.ipynb       # Model development
└── static/
    ├── images/                    # Dashboard images
    └── maps/                      # Generated maps
```

**Dataset Sources:**
- [Global Flood Database](https://global-flood-database.cloudtostreet.ai/)
- [NASA Flood Data](https://earthdata.nasa.gov/)
- [USGS Water Data](https://waterdata.usgs.gov/)

