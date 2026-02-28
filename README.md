## Nyne Flood Detection System

**Real-time flood risk prediction and early warning**
## Features

### Prerequisites
- Python 3.8+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/DaneenaR/flood-detection.git
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

**3. Open-Elevation**
-Unlimited free usage
-No sign-up required

### Run the App

```bash
# Start Streamlit dashboard
streamlit run app.py
```

Open http://localhost:8501 in your browser

## How It Works

### 1. **Data Collection**
```
User Input (Location): Satellite Imagery, weather forecast, & elevation data
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

**Dataset Sources:**
- [Global Flood Database](https://global-flood-database.cloudtostreet.ai/)
- [NASA Flood Data](https://earthdata.nasa.gov/)
- [USGS Water Data](https://waterdata.usgs.gov/)

