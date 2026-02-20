# 🌊 AI-Powered Flood Detection System

**Multi-modal AI system for real-time flood risk prediction and early warning**

![Demo](static/images/demo.png)

## ✨ Features

### 🛰️ **Satellite Analysis**
- Real-time satellite imagery from Sentinel Hub
- Water body detection using NDWI (Normalized Difference Water Index)
- Land cover change detection
- Cloud coverage assessment

### 🌦️ **Weather Integration**
- Live weather forecasts (7-day)
- Rainfall predictions and tracking
- Temperature and humidity monitoring
- Storm alert integration

### ⛰️ **Terrain Analysis**
- Elevation profile mapping
- Slope calculation for runoff assessment
- Low-lying area identification
- Coastal flood risk evaluation

### 🤖 **AI Prediction Model**
- Multi-modal deep learning
- Real-time risk scoring (0-100%)
- Timeline forecasting
- Confidence intervals

### 📊 **Interactive Dashboard**
- Real-time risk maps
- Risk factor breakdown
- Historical trends
- Actionable recommendations

## 💰 Cost: $0.00

| Service | Free Tier | Usage |
|---------|-----------|-------|
| **Sentinel Hub** | 1000 req/month | Satellite imagery |
| **OpenWeatherMap** | 1000 calls/day | Weather data |
| **Open-Elevation** | Unlimited | Elevation data |
| **Streamlit** | Free hosting | Dashboard |
| **Hugging Face** | Free hosting | Deployment |

## 🚀 Quick Start

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

Open http://localhost:8501 in your browser! 🎉

## 📖 How It Works

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

## 🎯 Use Cases

### 🏘️ **Community Safety**
- Early warning for residential areas
- Evacuation planning
- Resource allocation

### 🏢 **Business Continuity**
- Facility risk assessment
- Insurance underwriting
- Supply chain planning

### 🏛️ **Government & Emergency**
- Disaster response coordination
- Infrastructure protection
- Public safety alerts

### 🌾 **Agriculture**
- Crop protection
- Irrigation planning
- Harvest timing

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Maps** | Folium, Leaflet |
| **Data Processing** | Pandas, NumPy |
| **Geospatial** | GeoPandas, Rasterio |
| **Visualization** | Plotly, Matplotlib |
| **ML Framework** | TensorFlow / PyTorch |
| **APIs** | Sentinel Hub, OpenWeatherMap |

## 📁 Project Structure

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

## 🔬 Model Training (Optional)

The system works with mock predictions out-of-the-box. To train a real model:

```bash
# Download historical flood data
python scripts/download_data.py

# Train model
python scripts/train_model.py

# Evaluate
python scripts/evaluate.py
```

**Dataset Sources:**
- [Global Flood Database](https://global-flood-database.cloudtostreet.ai/)
- [NASA Flood Data](https://earthdata.nasa.gov/)
- [USGS Water Data](https://waterdata.usgs.gov/)

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free!)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. Go to share.streamlit.io
# 3. Connect GitHub repo
# 4. Add secrets (API keys)
# 5. Deploy!
```

### Deploy to Hugging Face Spaces

```bash
# 1. Create Space at huggingface.co
# 2. Select Streamlit SDK
# 3. Push code
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/flood-detection
git push hf main

# 4. Add secrets in Space settings
```

## 📸 Screenshots

### Interactive Risk Map
![Map](static/images/map_demo.png)

### Risk Analysis Dashboard
![Dashboard](static/images/dashboard_demo.png)

### Weather Forecast
![Weather](static/images/weather_demo.png)

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Real-time alert system (email/SMS)
- [ ] Mobile app version
- [ ] Integration with more data sources
- [ ] Improved ML model accuracy
- [ ] Multi-language support
- [ ] Historical disaster database
- [ ] Community reporting features

## 📄 License

MIT License - free for personal and commercial use

## 🙏 Acknowledgments

- **Sentinel Hub** for satellite imagery API
- **OpenWeatherMap** for weather data
- **Open-Elevation** for elevation data
- **Streamlit** for dashboard framework

## 📞 Contact

- **GitHub:** [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- **LinkedIn:** [Your Profile](https://linkedin.com/in/YOUR_PROFILE)
- **Portfolio:** [your-portfolio.com](https://your-portfolio.com)

---

**🌊 Making communities safer through AI-powered early warning systems**

*Built with ❤️ for disaster prevention and public safety*
