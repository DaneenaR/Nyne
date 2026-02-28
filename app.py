import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from utils.satellite_data import get_satellite_imagery, analyze_water_bodies
from utils.weather_data import get_weather_forecast, get_rainfall_data
from utils.elevation_data import get_elevation_profile, calculate_flood_risk
from utils.ml_model import predict_flood_risk

#init session state
if 'results' not in st.session_state:
    st.session_state.results = None

#page config
st.set_page_config(
    page_title="Flood Detection",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        color: #1e88e5;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .risk-high {
        background-color: #ff5252;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
    }
    .risk-medium {
        background-color: #ffa726;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
    }
    .risk-low {
        background-color: #66bb6a;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Nyne</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Flood Risk Prediction & Early Warning</div>', unsafe_allow_html=True)

#initialise location in session state
if 'selected_lat' not in st.session_state:
    st.session_state.selected_lat = 40.7128
if 'selected_lon' not in st.session_state:
    st.session_state.selected_lon = -74.0060

#sidebar
with st.sidebar:
    st.title("Nyne - Flood Risk Prediction")
    st.subheader("Location")
    location_method = st.radio("Method:", ["Coordinates", "City Name", "Map"])

    if location_method == "Coordinates":
        latitude = st.number_input("Latitude", value=st.session_state.selected_lat, format="%.4f", key="lat_input")
        longitude = st.number_input("Longitude", value=st.session_state.selected_lon, format="%.4f", key="lon_input")
        location_name = "Custom Location"

        #updating session state
        st.session_state.selected_lat = latitude
        st.session_state.selected_lon = longitude


    elif location_method == "City Name":

        city_input = st.text_input("City name", placeholder="e.g., Kuala Lumpur, York, Milan")
        search_btn = st.button("Search", type="secondary")
        if city_input and search_btn:
            try:
                from geopy.geocoders import Nominatim
                import time
                with st.spinner(f"Finding {city_input}..."):
                    #better user agent with contact info
                    geolocator = Nominatim(
                        user_agent="nyne-dev@gmail.com",
                        timeout=10
                    )

                    #delay for rate llimits
                    time.sleep(1)
                    location = geolocator.geocode(city_input)
                    if location:
                        latitude = location.latitude
                        longitude = location.longitude
                        location_name = location.address
                        st.session_state.selected_lat = latitude
                        st.session_state.selected_lon = longitude
                        st.success(f"Found: {location_name}")
                        st.info(f"Coordinates: {latitude:.4f}, {longitude:.4f}")

                    else:
                        st.error(f"Could not find '{city_input}'. Try being more specific (e.g., 'Paris, France')")
                        latitude = st.session_state.selected_lat
                        longitude = st.session_state.selected_lon
                        location_name = "Unknown Location"


            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:
                    st.error("Too many requests. Please wait 60 seconds before searching again.")

                else:

                    st.error(f"Geocoding error: {error_msg}")
                    latitude = st.session_state.selected_lat
                    longitude = st.session_state.selected_lon
                    location_name = "Unknown Location"

        else:

            #search has not existed yet, use last known location
            latitude = st.session_state.selected_lat
            longitude = st.session_state.selected_lon
            location_name = "Enter a city name and click Search"
            if not search_btn:
                st.info("Type a city name and click 'Search'")
    #map
    else:
        latitude = st.session_state.selected_lat
        longitude = st.session_state.selected_lon
        location_name = f"Map Selected ({latitude:.4f}, {longitude:.4f})"
        st.info(f"Lat: {latitude:.4f}, Lon: {longitude:.4f}")

    #analysis parameters
    st.subheader("Parameters")
    analysis_days = st.slider("Forecast days", 1, 7, 3)
    sensitivity = st.select_slider("Risk sensitivity",
                                   options=["Low", "Medium", "High"],
                                   value="Medium")

    #data sources
    st.subheader("Data Sources")
    use_satellite = st.checkbox("Satellite imagery", value=True)
    use_weather = st.checkbox("Weather data", value=True)
    use_elevation = st.checkbox("Elevation data", value=True)
    use_historical = st.checkbox("Historical floods", value=True)
    analyze_btn = st.button("Analyse", type="primary", use_container_width=True)

#show map selection interface if Map is selected
if location_method == "Map " and st.session_state.results is None:
    st.markdown("---")
    st.subheader("Click on the map to select a location")

    st.info(f"Current selection: Latitude {st.session_state.selected_lat:.4f}, Longitude {st.session_state.selected_lon:.4f}")

    #create selection map
    selection_map = folium.Map(
        location=[st.session_state.selected_lat, st.session_state.selected_lon],
        zoom_start=4,
        tiles="OpenStreetMap"
    )

    #add current marker
    folium.Marker(
        [st.session_state.selected_lat, st.session_state.selected_lon],
        popup="Click anywhere on map to select new location",
        icon=folium.Icon(color='blue', icon='map-marker')
    ).add_to(selection_map)

    #display map and capture clicks
    map_data = st_folium(selection_map, width=1200, height=500, key="location_selector")

    #update the location if map was clicked
    if map_data and map_data.get('last_clicked'):
        new_lat = map_data['last_clicked']['lat']
        new_lon = map_data['last_clicked']['lng']

        #update only if location changed
        if abs(new_lat - st.session_state.selected_lat) > 0.0001 or abs(new_lon - st.session_state.selected_lon) > 0.0001:
            st.session_state.selected_lat = new_lat
            st.session_state.selected_lon = new_lon
            st.success(f"Location updated! New coordinates: {new_lat:.4f}, {new_lon:.4f}")
            st.rerun()

    st.markdown("---")
    st.info("After selecting location, click 'Analyse Flood Risk' in the sidebar")

#main content
if analyze_btn:
    with st.spinner("Analysing flood risk... This may take 30-60 seconds"):

        progress_bar = st.progress(0)
        status_text = st.empty()
        #satellite data
        if use_satellite:
            status_text.text("Fetching satellite imagery...")
            progress_bar.progress(20)
            satellite_data = get_satellite_imagery(latitude, longitude)
            water_analysis = analyze_water_bodies(satellite_data)
        else:
            satellite_data = None
            water_analysis = None

        #weather data
        if use_weather:
            status_text.text("Getting weather forecast...")
            progress_bar.progress(40)
            weather_data = get_weather_forecast(latitude, longitude, days=analysis_days)
            rainfall_data = get_rainfall_data(latitude, longitude)
        else:
            weather_data = None
            rainfall_data = None

        #elevation data
        if use_elevation:
            status_text.text("Analysing elevation profile...")
            progress_bar.progress(60)
            elevation_data = get_elevation_profile(latitude, longitude, radius_km=5)
            terrain_risk = calculate_flood_risk(elevation_data)
        else:
            elevation_data = None
            terrain_risk = None

        #ml prediction
        status_text.text("Running AI model...")
        progress_bar.progress(80)

        # Combine all data
        features = {
            'satellite': satellite_data if use_satellite else None,
            'weather': weather_data if use_weather else None,
            'elevation': elevation_data if use_elevation else None,
            'location': (latitude, longitude)
        }

        flood_risk = predict_flood_risk(features, sensitivity=sensitivity)

        st.session_state.results = {
            'flood_risk': flood_risk,
            'satellite_data': satellite_data,
            'water_analysis': water_analysis,
            'weather_data': weather_data,
            'elevation_data': elevation_data,
            'latitude': latitude,
            'longitude': longitude,
            'location_name': location_name,
            'analysis_days': analysis_days,
            'use_satellite': use_satellite,
            'use_weather': use_weather,
            'use_elevation': use_elevation,
            'use_historical': use_historical
        }

        progress_bar.progress(100)
        status_text.text("Analysis complete!")
#display results
if st.session_state.results is not None:
    #load from session state
    flood_risk = st.session_state.results['flood_risk']
    satellite_data = st.session_state.results['satellite_data']
    water_analysis = st.session_state.results['water_analysis']
    weather_data = st.session_state.results['weather_data']
    elevation_data = st.session_state.results['elevation_data']
    latitude = st.session_state.results['latitude']
    longitude = st.session_state.results['longitude']
    location_name = st.session_state.results['location_name']
    analysis_days = st.session_state.results['analysis_days']
    use_satellite = st.session_state.results['use_satellite']
    use_weather = st.session_state.results['use_weather']
    use_elevation = st.session_state.results['use_elevation']
    use_historical = st.session_state.results['use_historical']

    st.markdown("---")

    #risk level display
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        risk_level = flood_risk['level']  #high,med,low
        risk_score = flood_risk['score']  #0-100

        if risk_level == 'HIGH':
            st.markdown(f'<div class="risk-high">HIGH FLOOD RISK<br>{risk_score}% Probability</div>',
                       unsafe_allow_html=True)
        elif risk_level == 'MEDIUM':
            st.markdown(f'<div class="risk-medium">MEDIUM FLOOD RISK<br>{risk_score}% Probability</div>',
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="risk-low">LOW FLOOD RISK<br>{risk_score}% Probability</div>',
                       unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Map",
        "Risk Analysis",
        "Satellite Data",
        "Weather Forecast",
        "Historical Trends"
    ])

    with tab1:
        st.subheader("Flood Risk Map")

        #create folium map
        m = folium.Map(
            location=[latitude, longitude],
            zoom_start=12,
            tiles="OpenStreetMap"
        )

        #risk circle
        color = 'red' if risk_level == 'HIGH' else 'orange' if risk_level == 'MEDIUM' else 'green'
        folium.Circle(
            location=[latitude, longitude],
            radius=2000,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.3,
            popup=f"Risk: {risk_level}"
        ).add_to(m)

        #marker
        folium.Marker(
            [latitude, longitude],
            popup=f"{location_name}<br>Risk: {risk_score}%",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)

        #display map
        st_folium(m, width=1200, height=500)

    with tab2:
        st.subheader("Risk Factors Breakdown")

        col1, col2 = st.columns(2)

        with col1:
            #risk factors pie chart
            factors = flood_risk['factors']
            fig = px.pie(
                values=list(factors.values()),
                names=list(factors.keys()),
                title="Contributing Factors"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            #risk timeline
            timeline_data = flood_risk['timeline']
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=timeline_data['dates'],
                y=timeline_data['risk_scores'],
                mode='lines+markers',
                name='Risk Level',
                line=dict(color='red', width=3)
            ))
            fig.update_layout(
                title=f"Risk Forecast (Next {analysis_days} Days)",
                xaxis_title="Date",
                yaxis_title="Risk Score (%)",
                yaxis_range=[0, 100]
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Recommendations")
        for rec in flood_risk['recommendations']:
            st.info(f"• {rec}")

    with tab3:
        if use_satellite:
            st.subheader("Satellite Imagery Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.image(satellite_data['image'], caption="Recent Satellite Image")

            with col2:
                st.metric("Water Coverage", f"{water_analysis['water_percentage']:.1f}%")
                st.metric("Change from Last Month", f"{water_analysis['change']:.1f}%")
                st.metric("Risk Indicators", water_analysis['risk_count'])

            st.write("**Analysis:**", water_analysis['analysis'])

    with tab4:
        if use_weather:
            st.subheader("Weather Forecast")

            #rainfall chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=weather_data['dates'],
                y=weather_data['rainfall_mm'],
                name='Expected Rainfall (mm)',
                marker_color='blue'
            ))
            fig.update_layout(
                title="Rainfall Forecast",
                xaxis_title="Date",
                yaxis_title="Rainfall (mm)"
            )
            st.plotly_chart(fig, use_container_width=True)

            #weather summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rainfall", f"{sum(weather_data['rainfall_mm']):.1f} mm")
            with col2:
                st.metric("Peak Day", f"{max(weather_data['rainfall_mm']):.1f} mm")
            with col3:
                st.metric("Humidity", f"{weather_data['avg_humidity']:.1f}%")

    with tab5:
        if use_historical:
            st.subheader("Historical Flood Data")

            #mock historical data
            years = list(range(2015, 2025))
            floods = [2, 1, 3, 0, 2, 1, 4, 2, 1, 3]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=years,
                y=floods,
                name='Flood Events',
                marker_color='lightblue'
            ))
            fig.update_layout(
                title="Historical Flood Events (10 Years)",
                xaxis_title="Year",
                yaxis_title="Number of Events"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.info(f"Average flood events per year in this area: {np.mean(floods):.1f}")

else:
    #welcome screen only show if no results
    st.info("Configure settings in the sidebar and click 'Analyse Flood Risk' to begin")

    #feature highlights
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Satellite Analysis")
        st.write("Real-time satellite imagery from Sentinel Hub")
        st.write("• Water body detection")
        st.write("• Land cover changes")
        st.write("• NDWI index calculation")

    with col2:
        st.markdown("### Weather Integration")
        st.write("Live weather data and forecasts")
        st.write("• Rainfall predictions")
        st.write("• Temperature & humidity")
        st.write("• Storm tracking")

    with col3:
        st.markdown("### AI Prediction")
        st.write("Machine learning risk assessment")
        st.write("• Multi-modal analysis")
        st.write("• Historical patterns")
        st.write("• Real-time alerts")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>© 2026 Daneena Roy. UI by Streamlit . Nyne - Flood Risk Prediction and Early Warning</p>
</div>
""", unsafe_allow_html=True)