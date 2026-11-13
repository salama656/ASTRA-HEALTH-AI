
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

import streamlit.components.v1 as components
import base64
from pathlib import Path
from sklearn.ensemble import IsolationForest

# =========================================================
# ASTRA HEALTH AI | FUTURISTIC SPACE MEDICAL COMMAND CENTER
# Student research prototype - simulated data only
# =========================================================

st.set_page_config(
    page_title="ASTRA HEALTH AI | Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- DESIGN SYSTEM --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg: #050914;
    --panel: rgba(12, 25, 47, 0.88);
    --cyan: #38dcff;
    --blue: #398bff;
    --purple: #9875ff;
    --green: #3ce6b0;
    --muted: #829bb9;
    --border: rgba(65, 183, 255, 0.20);
}

.stApp {
    background:
        radial-gradient(ellipse at 12% 10%, rgba(0, 117, 255, 0.17), transparent 32%),
        radial-gradient(ellipse at 90% 20%, rgba(0, 226, 255, 0.10), transparent 30%),
        radial-gradient(ellipse at 50% 90%, rgba(100, 65, 255, 0.09), transparent 40%),
        #050914;
    color: #edf7ff;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1600px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f1f8ff !important;
}

h1 {
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 3px !important;
    font-weight: 800 !important;
}

h2, h3 {
    font-family: 'Inter', sans-serif !important;
}

p, label, span {
    color: #c5d7ed;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1930, #060d1b);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #e9f8ff !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(19, 43, 73, 0.95), rgba(8, 19, 37, 0.96));
    border: 1px solid rgba(56, 220, 255, 0.25);
    border-radius: 17px;
    padding: 17px 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.24);
    transition: all .25s ease;
}

[data-testid="stMetric"]:hover {
    border-color: var(--cyan);
    box-shadow: 0 0 24px rgba(56, 220, 255, 0.16);
    transform: translateY(-3px);
}

[data-testid="stMetricLabel"] {
    color: #91b3d5 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 1.1px;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Orbitron', sans-serif;
    font-size: 27px !important;
}

[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

div[data-testid="stPlotlyChart"] {
    background: rgba(8, 19, 37, 0.55);
    border: 1px solid rgba(56, 220, 255, 0.16);
    border-radius: 17px;
    padding: 8px;
}

.stSelectbox > div > div {
    background: #10233d;
    border: 1px solid #24476d;
    border-radius: 10px;
}

.stButton > button {
    background: linear-gradient(90deg, #0878e8, #00bdd8);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

.stButton > button:hover {
    box-shadow: 0 0 20px rgba(0, 185, 216, 0.35);
    color: white;
}

hr {
    border-color: rgba(75, 153, 220, 0.18);
}

.stCaption {
    color: #7894b5 !important;
}

[data-testid="stAlert"] {
    border-radius: 13px;
}

div[data-testid="stExpander"] {
    background: rgba(12, 25, 47, 0.7);
    border: 1px solid var(--border);
    border-radius: 13px;
}

footer, #MainMenu {
    visibility: hidden;
}

.hero {
    background:
        radial-gradient(circle at 85% 20%, rgba(0, 194, 255, .17), transparent 35%),
        linear-gradient(120deg, rgba(14, 35, 65, .96), rgba(7, 17, 34, .96));
    border: 1px solid rgba(56, 220, 255, .30);
    border-radius: 22px;
    padding: 27px 30px;
    margin-bottom: 17px;
    box-shadow: 0 0 35px rgba(0, 120, 255, .08);
}

.eyebrow {
    color: #43dfff;
    font-family: 'Orbitron', sans-serif;
    font-size: 11px;
    letter-spacing: 3px;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(25px, 3vw, 42px);
    font-weight: 800;
    color: #f5fbff;
    letter-spacing: 2px;
    margin: 9px 0;
}

.hero-sub {
    color: #9bb7d5;
    font-size: 14px;
}

.status-pill {
    display: inline-block;
    padding: 7px 13px;
    border: 1px solid rgba(60, 230, 176, .45);
    border-radius: 30px;
    color: #63efc2;
    background: rgba(60, 230, 176, .08);
    font-size: 11px;
    letter-spacing: 1px;
    font-weight: 700;
}

.section-heading {
    font-family: 'Orbitron', sans-serif;
    font-size: 17px;
    color: #eaf8ff;
    letter-spacing: 1.3px;
    margin: 20px 0 4px 0;
}

.section-sub {
    font-size: 11px;
    color: #7895b6;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.info-panel {
    background: linear-gradient(145deg, rgba(17, 39, 68, .92), rgba(7, 18, 36, .94));
    border: 1px solid rgba(65, 183, 255, .22);
    border-radius: 17px;
    padding: 17px;
    min-height: 90px;
}

.panel-label {
    font-size: 10px;
    color: #7fa6ca;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.panel-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 22px;
    color: #eafaff;
    margin-top: 7px;
}

.panel-note {
    font-size: 11px;
    color: #7996b5;
    margin-top: 4px;
}

.alert-box {
    background: linear-gradient(100deg, rgba(255, 166, 55, .12), rgba(255, 90, 70, .04));
    border: 1px solid rgba(255, 166, 55, .38);
    border-left: 4px solid #ffad42;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.safe-box {
    background: rgba(45, 210, 157, .08);
    border: 1px solid rgba(60, 230, 176, .30);
    border-left: 4px solid #3ce6b0;
    padding: 15px;
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: #617f9f;
    padding: 25px;
    font-size: 11px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# -------------------- MISSION SCENARIOS --------------------

SCENARIOS = {
    "Normal mission conditions": {
        "hr": 76, "spo2": 98, "temp": 36.8,
        "sleep": 7.5, "radiation": 0.8,
        "stress": 25, "activity": 45, "bone": 94,
        "isolation": 20, "microgravity": 70
    },

    "Elevated heart rate": {
        "hr": 118, "spo2": 97, "temp": 36.9,
        "sleep": 7.2, "radiation": 0.9,
        "stress": 65, "activity": 30, "bone": 94,
        "isolation": 25, "microgravity": 70
    },

    "Reduced oxygen saturation": {
        "hr": 92, "spo2": 90, "temp": 36.8,
        "sleep": 7.0, "radiation": 0.8,
        "stress": 45, "activity": 25, "bone": 94,
        "isolation": 25, "microgravity": 70
    },

    "Elevated body temperature": {
        "hr": 96, "spo2": 97, "temp": 38.0,
        "sleep": 6.5, "radiation": 0.8,
        "stress": 55, "activity": 20, "bone": 94,
        "isolation": 25, "microgravity": 70
    },

    "Insufficient sleep": {
        "hr": 88, "spo2": 98, "temp": 36.7,
        "sleep": 3.2, "radiation": 0.9,
        "stress": 72, "activity": 15, "bone": 94,
        "isolation": 35, "microgravity": 70
    },

    "Increased radiation exposure": {
        "hr": 82, "spo2": 98, "temp": 36.8,
        "sleep": 7.2, "radiation": 3.5,
        "stress": 35, "activity": 35, "bone": 93,
        "isolation": 25, "microgravity": 70
    },

    "Microgravity & bone health": {
        "hr": 84, "spo2": 98, "temp": 36.8,
        "sleep": 7.0, "radiation": 1.0,
        "stress": 40, "activity": 20, "bone": 78,
        "isolation": 30, "microgravity": 100
    },

    "Isolation & elevated stress": {
        "hr": 94, "spo2": 98, "temp": 36.8,
        "sleep": 5.2, "radiation": 0.9,
        "stress": 88, "activity": 15, "bone": 92,
        "isolation": 90, "microgravity": 70
    }
}


# -------------------- SIDEBAR --------------------

st.sidebar.markdown("""
<div style="font-family:Orbitron; color:#42ddff; font-size:20px;
letter-spacing:2px; font-weight:800;">
ASTRA CONTROL
</div>
<div style="color:#7896b7; font-size:11px; letter-spacing:1px;">
SPACE MEDICAL COMMAND
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

astronaut = st.sidebar.selectbox(
    "ASTRONAUT PROFILE",
    ["Astronaut 01", "Astronaut 02", "Astronaut 03"]
)

mission = st.sidebar.selectbox(
    "MISSION SCENARIO",
    list(SCENARIOS.keys())
)

st.sidebar.divider()

st.sidebar.markdown("### MISSION DETAILS")
st.sidebar.markdown("""
**MISSION ID**  
ORBIT-01

**LOCATION**  
Low Earth Orbit

**MISSION STATUS**  
:green[● ACTIVE SIMULATION]

**DATA SOURCE**  
Synthetic telemetry
""")

st.sidebar.divider()

st.sidebar.markdown("### SYSTEM MODULES")
st.sidebar.markdown("""
🫀 Cardiovascular monitoring

🫁 Oxygen monitoring

🌡 Temperature monitoring

🧠 Wellbeing and isolation indicators

🦴 Bone health simulation

☢️ Radiation exposure simulation

🌌 Microgravity exposure indicator

🤖 AI anomaly detection
""")

st.sidebar.info(
    "Select a mission scenario to simulate different astronaut conditions."
)

profile = SCENARIOS[mission]


# -------------------- SIMULATED TELEMETRY --------------------

rng = np.random.default_rng(42)

hours = 24

timestamps = [
    datetime.now() - timedelta(hours=23-i)
    for i in range(hours)
]

heart_rate = rng.normal(76, 5, hours)
oxygen = rng.normal(98, 0.7, hours)
temperature = rng.normal(36.7, 0.15, hours)

radiation = rng.normal(0.8, 0.12, hours)
stress = rng.normal(25, 5, hours)
activity = rng.normal(45, 8, hours)
bone = rng.normal(94, 1.5, hours)
isolation = rng.normal(20, 5, hours)
microgravity = rng.normal(70, 5, hours)

# Apply selected scenario to the latest four readings.
heart_rate[-4:] = rng.normal(profile["hr"], 2, 4)
oxygen[-4:] = rng.normal(profile["spo2"], 0.4, 4)
temperature[-4:] = rng.normal(profile["temp"], 0.08, 4)

radiation[-4:] = rng.normal(profile["radiation"], 0.05, 4)
stress[-4:] = rng.normal(profile["stress"], 2, 4)
activity[-4:] = rng.normal(profile["activity"], 2, 4)
bone[-4:] = rng.normal(profile["bone"], 0.5, 4)
isolation[-4:] = rng.normal(profile["isolation"], 2, 4)
microgravity[-4:] = rng.normal(profile["microgravity"], 1, 4)

# Keep generated values within illustrative ranges.
heart_rate = np.clip(heart_rate, 45, 160)
oxygen = np.clip(oxygen, 80, 100)
temperature = np.clip(temperature, 34, 41)

radiation = np.clip(radiation, 0, 5)
stress = np.clip(stress, 0, 100)
activity = np.clip(activity, 0, 180)
bone = np.clip(bone, 0, 100)
isolation = np.clip(isolation, 0, 100)
microgravity = np.clip(microgravity, 0, 100)

sleep = profile["sleep"]

df = pd.DataFrame({
    "Time": timestamps,
    "Heart Rate": heart_rate,
    "Oxygen Saturation": oxygen,
    "Temperature": temperature,
    "Sleep": [sleep] * hours,
    "Radiation Exposure Index": radiation,
    "Stress Indicator": stress,
    "Physical Activity": activity,
    "Bone Health Index": bone,
    "Isolation Indicator": isolation,
    "Microgravity Exposure": microgravity
})

current_hr = float(heart_rate[-1])
current_spo2 = float(oxygen[-1])
current_temp = float(temperature[-1])
current_radiation = float(radiation[-1])
current_stress = float(stress[-1])
current_activity = float(activity[-1])
current_bone = float(bone[-1])
current_isolation = float(isolation[-1])
current_microgravity = float(microgravity[-1])


# -------------------- MACHINE LEARNING --------------------

baseline = pd.DataFrame({
    "Heart Rate": rng.normal(76, 5, 1000),
    "Oxygen Saturation": rng.normal(98, 0.7, 1000),
    "Temperature": rng.normal(36.7, 0.15, 1000),
    "Sleep": rng.normal(7.5, 0.8, 1000),
    "Radiation Exposure Index": rng.normal(0.8, 0.15, 1000),
    "Stress Indicator": rng.normal(25, 8, 1000),
    "Physical Activity": rng.normal(45, 10, 1000),
    "Bone Health Index": rng.normal(94, 2, 1000),
    "Isolation Indicator": rng.normal(20, 8, 1000),
    "Microgravity Exposure": rng.normal(70, 5, 1000)
})

current_data = pd.DataFrame([{
    "Heart Rate": current_hr,
    "Oxygen Saturation": current_spo2,
    "Temperature": current_temp,
    "Sleep": sleep,
    "Radiation Exposure Index": current_radiation,
    "Stress Indicator": current_stress,
    "Physical Activity": current_activity,
    "Bone Health Index": current_bone,
    "Isolation Indicator": current_isolation,
    "Microgravity Exposure": current_microgravity
}])

model = IsolationForest(
    contamination=0.04,
    random_state=42
)

model.fit(baseline)

prediction = model.predict(current_data)[0]
anomaly_detected = prediction == -1


# -------------------- EXPLAINABLE AI --------------------

baseline_mean = baseline.mean()
baseline_std = baseline.std().replace(0, 1)

deviation_rows = []

for metric in current_data.columns:
    value = float(current_data.iloc[0][metric])
    mean = float(baseline_mean[metric])
    std = float(baseline_std[metric])

    z_score = (value - mean) / std

    if abs(z_score) >= 2:
        deviation_rows.append({
            "Health Indicator": metric,
            "Current Reading": round(value, 2),
            "Baseline Average": round(mean, 2),
            "Difference (standard deviations)": round(z_score, 2)
        })


# -------------------- ALERT ENGINE --------------------

alerts = []

if current_hr > 110:
    alerts.append((
        "HEART RATE VARIATION",
        "The simulated heart rate is above the illustrative demo threshold."
    ))

if current_spo2 < 94:
    alerts.append((
        "OXYGEN SATURATION VARIATION",
        "The simulated oxygen reading is below the illustrative demo threshold."
    ))

if current_temp > 37.8:
    alerts.append((
        "TEMPERATURE VARIATION",
        "The simulated body temperature is above the illustrative demo threshold."
    ))

if sleep < 5:
    alerts.append((
        "SLEEP DURATION",
        "The simulated sleep duration is below the illustrative demo target."
    ))

if current_radiation > 2.0:
    alerts.append((
        "RADIATION EXPOSURE VARIATION",
        "The simulated radiation exposure index is above the illustrative demo threshold."
    ))

if current_bone < 85:
    alerts.append((
        "BONE HEALTH INDICATOR",
        "The simulated bone health index is below the illustrative demo threshold."
    ))

if current_microgravity > 90:
    alerts.append((
        "MICROGRAVITY EXPOSURE",
        "The simulated microgravity exposure indicator is elevated."
    ))

if current_stress > 75:
    alerts.append((
        "ELEVATED STRESS INDICATOR",
        "The simulated wellbeing indicator is above the illustrative demo threshold."
    ))

if current_isolation > 75:
    alerts.append((
        "ISOLATION INDICATOR",
        "The simulated isolation indicator is above the illustrative demo threshold."
    ))

if current_activity < 15:
    alerts.append((
        "LOW PHYSICAL ACTIVITY",
        "The simulated activity level is below the illustrative demo target."
    ))

if anomaly_detected and not alerts:
    alerts.append((
        "AI ANOMALY DETECTED",
        "The machine-learning model identified an unusual combination of simulated readings."
    ))


# -------------------- PLOTLY THEME --------------------

def chart_layout(fig, height=300):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter",
            color="#a9c4df",
            size=11
        ),
        margin=dict(l=15, r=15, t=35, b=15),
        height=height,
        legend=dict(
            orientation="h",
            y=1.13,
            x=0
        ),
        hoverlabel=dict(
            bgcolor="#10243d",
            bordercolor="#38dcff",
            font_color="white"
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(100,160,210,0.10)",
        zeroline=False
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(100,160,210,0.10)",
        zeroline=False
    )
    return fig


# =========================================================
# 3D ASTRONAUT SKELETON
# =========================================================

def render_skeleton():
    skeleton_path = Path(__file__).parent / "skeleton.glb"

    if not skeleton_path.exists():
        st.error(f"Skeleton model not found: {skeleton_path}")
        return

    file_size = skeleton_path.stat().st_size

    if file_size < 100:
        st.error("The skeleton model file appears to be empty.")
        return

    with open(skeleton_path, "rb") as file:
        model_data = base64.b64encode(file.read()).decode("ascii")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <script type="module"
        src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js">
        </script>

        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background: transparent;
            }}

            model-viewer {{
                display: block;
                width: 100%;
                height: 470px;
                background: transparent;
                --poster-color: transparent;
            }}

            #loading {{
                position: absolute;
                top: 15px;
                left: 15px;
                color: #38dcff;
                font-family: Arial;
                font-size: 12px;
                z-index: 5;
            }}

            #error {{
                color: #ff7777;
                font-family: Arial;
                font-size: 13px;
                padding: 15px;
            }}
        </style>
    </head>

    <body>

        <div id="loading">INITIALIZING 3D SKELETON...</div>

        <model-viewer
            id="skeleton"
            src="data:model/gltf-binary;base64,{model_data}"
            camera-controls
            auto-rotate
            rotation-per-second="15deg"
            shadow-intensity="1"
            exposure="1.2"
            environment-image="neutral"
            camera-orbit="0deg 75deg auto"
            interaction-prompt="auto"
            reveal="auto"
        >
        </model-viewer>

        <script>
            const viewer = document.getElementById("skeleton");
            const loading = document.getElementById("loading");

            viewer.addEventListener("load", () => {{
                loading.textContent = "3D SKELETON ONLINE";
            }});

            viewer.addEventListener("error", (event) => {{
                loading.textContent = "MODEL LOADING FAILED";
                document.body.insertAdjacentHTML(
                    "beforeend",
                    '<div id="error">The 3D model could not be displayed. Check the browser console for details.</div>'
                );
                console.error("Skeleton model error:", event);
            }});
        </script>

    </body>
    </html>
    """

    components.html(html, height=490, scrolling=False)


# =========================================================
# 3D EARTH GLOBE
# =========================================================

def make_earth():
    lon = np.linspace(-180, 180, 100)
    lat = np.linspace(-90, 90, 70)

    lon_grid, lat_grid = np.meshgrid(lon, lat)

    lon_rad = np.radians(lon_grid)
    lat_rad = np.radians(lat_grid)

    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)

    land = np.zeros_like(lon_grid)

    continents = [
        (-100, 45, 38, 22),
        (-65, -15, 22, 35),
        (20, 5, 35, 25),
        (80, 45, 65, 25),
        (135, -25, 25, 18),
        (45, 45, 20, 15)
    ]

    for center_lon, center_lat, width, height in continents:
        distance = (
            ((lon_grid - center_lon) / width) ** 2
            + ((lat_grid - center_lat) / height) ** 2
        )
        land = np.maximum(land, np.exp(-distance * 2))

    surface_color = land * 0.8 + 0.1

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        surfacecolor=surface_color,
        colorscale=[
            [0.0, "#06316b"],
            [0.35, "#0874ba"],
            [0.55, "#11a7bd"],
            [0.75, "#58d9bd"],
            [1.0, "#b0ffe0"]
        ],
        cmin=0,
        cmax=1,
        showscale=False,
        lighting=dict(
            ambient=0.45,
            diffuse=0.8,
            specular=0.65,
            roughness=0.45,
            fresnel=0.2
        ),
        lightposition=dict(x=2, y=3, z=4),
        hoverinfo="skip"
    ))

    theta = np.linspace(0, 2*np.pi, 250)

    fig.add_trace(go.Scatter3d(
        x=1.25*np.cos(theta),
        y=0.75*np.sin(theta),
        z=0.22*np.sin(theta),
        mode="lines",
        line=dict(color="#42ddff", width=3),
        showlegend=False,
        hoverinfo="skip"
    ))

    angle = 0.8

    fig.add_trace(go.Scatter3d(
        x=[1.25*np.cos(angle)],
        y=[0.75*np.sin(angle)],
        z=[0.22*np.sin(angle)],
        mode="markers",
        marker=dict(
            size=6,
            color="#ffffff",
            line=dict(color="#42ddff", width=3)
        ),
        name="Satellite",
        hovertemplate="ORBIT-01 satellite<extra></extra>"
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=390,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False, range=[-1.5, 1.5]),
            yaxis=dict(visible=False, range=[-1.5, 1.5]),
            zaxis=dict(visible=False, range=[-1.3, 1.3]),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.5, y=1.4, z=1.0))
        )
    )

    return fig


# =========================================================
# MAIN INTERFACE
# =========================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">SPACE MEDICAL INTELLIGENCE • ORBIT-01</div>
    <div class="hero-title">ASTRA HEALTH AI</div>
    <div class="hero-sub">
        Advanced Astronaut Health Monitoring & Predictive Intelligence System
    </div>
    <br>
    <span class="status-pill">● SYSTEM ONLINE</span>
    &nbsp;&nbsp;
    <span style="color:#8ca9c8;font-size:11px;">
    LOW EARTH ORBIT / SIMULATED TELEMETRY
    </span>
</div>
""", unsafe_allow_html=True)

st.warning(
    "SIMULATION ENVIRONMENT — All readings and visualizations are synthetic. "
    "This student prototype is not connected to real astronaut sensors "
    "and is not a medical diagnostic tool."
)


# =========================================================
# ASTRA MISSION INTRODUCTION VIDEO
# =========================================================

if "show_mission_video" not in st.session_state:
    st.session_state.show_mission_video = False

video_col1, video_col2, video_col3 = st.columns([1, 2, 1])

with video_col2:
    if st.button(
        "▶ WATCH ASTRA MISSION INTRODUCTION",
        key="astra_intro_button",
        use_container_width=True
    ):
        st.session_state.show_mission_video = True

if st.session_state.show_mission_video:

    video_path = (
        Path(__file__).resolve().parent
        / "ASTRA — THE MISSION EXPERIENCE.mp4"
    )

    if video_path.exists():
        st.markdown("### 🚀 ASTRA MISSION EXPERIENCE")

        st.video(str(video_path))

        if st.button("✕ CLOSE VIDEO", key="close_astra_intro"):
            st.session_state.show_mission_video = False
            st.rerun()

    else:
        st.error("Mission video not found.")
        st.write("ASTRA is looking for the video here:")
        st.code(str(video_path))

st.markdown("---")


# Mission summary
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("ASTRONAUT", astronaut)

with s2:
    st.metric("MISSION ID", "ORBIT-01")

with s3:
    st.metric("ORBIT LOCATION", "LEO")

with s4:
    st.metric("AI ENGINE", "ACTIVE")

st.markdown("---")


# =========================================================
# HOLOGRAPHIC VISUALIZATION SECTION
# =========================================================

st.markdown("""
<div class="section-heading">01 / HOLOGRAPHIC MISSION VIEW</div>
<div class="section-sub">ASTRONAUT BIOMETRICS • EARTH ORBIT VISUALIZATION</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.05, 1])

with left:
    st.markdown("""
    <div class="info-panel">
        <div class="panel-label">ASTRONAUT BODY SCAN</div>
        <div style="color:#38dcff;font-size:11px;margin-top:5px;">
        3D BIOMETRIC MONITORING MODEL
        </div>
    </div>
    """, unsafe_allow_html=True)

    render_skeleton()

    st.caption(
        "Stylized anatomical visualization. Monitoring points are illustrative, "
        "not actual sensor locations."
    )

with right:
    st.markdown("""
    <div class="info-panel">
        <div class="panel-label">EARTH / ORBITAL VIEW</div>
        <div style="color:#38dcff;font-size:11px;margin-top:5px;">
        LOW EARTH ORBIT • ORBIT-01
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        make_earth(),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown("""
    <div class="info-panel">
        <div class="panel-label">MISSION ENVIRONMENT</div>
        <div class="panel-value" style="font-size:17px;">
        LOW EARTH ORBIT
        </div>
        <div class="panel-note">
        Orbital mission simulation • Earth observation • Crew health telemetry
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# BIOMETRIC MONITORING
# =========================================================

st.markdown("---")
st.markdown("""
<div class="section-heading">02 / LIVE BIOMETRIC TELEMETRY</div>
<div class="section-sub">LATEST SIMULATED ASTRONAUT HEALTH READINGS</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("♥ HEART RATE", f"{current_hr:.0f} bpm")

with m2:
    st.metric("◉ OXYGEN SATURATION", f"{current_spo2:.1f}%")

with m3:
    st.metric("⌁ BODY TEMPERATURE", f"{current_temp:.1f} °C")

with m4:
    st.metric("◷ SLEEP DURATION", f"{sleep:.1f} hrs")

# Additional mission indicators
b1, b2, b3, b4, b5 = st.columns(5)

with b1:
    st.metric(
        "RADIATION EXPOSURE INDEX",
        f"{current_radiation:.2f}/5"
    )

with b2:
    st.metric(
        "STRESS INDICATOR",
        f"{current_stress:.0f}/100"
    )

with b3:
    st.metric(
        "DAILY ACTIVITY",
        f"{current_activity:.0f} min"
    )

with b4:
    st.metric(
        "ISOLATION INDICATOR",
        f"{current_isolation:.0f}/100"
    )

with b5:
    st.metric(
        "MICROGRAVITY INDICATOR",
        f"{current_microgravity:.0f}/100"
    )


# =========================================================
# AI INTELLIGENCE CENTER
# =========================================================

st.markdown("---")
st.markdown("""
<div class="section-heading">03 / AI INTELLIGENCE CENTER</div>
<div class="section-sub">MACHINE LEARNING • ANOMALY DETECTION • EXPLAINABLE AI</div>
""", unsafe_allow_html=True)

ai1, ai2 = st.columns([1, 1])

with ai1:
    if anomaly_detected:
        st.error("AI STATUS: ANOMALY DETECTED")
        st.write(
            "The Isolation Forest model identified a pattern "
            "that differs from its synthetic baseline."
        )
    else:
        st.success("AI STATUS: BASELINE PATTERN")
        st.write(
            "The model did not flag the latest simulated readings "
            "as anomalous."
        )

with ai2:
    if alerts:
        st.warning(f"WARNING CENTER: {len(alerts)} ALERT(S)")
        st.write("One or more illustrative thresholds have been crossed.")
    else:
        st.success("WARNING CENTER: NO DEMO ALERTS")
        st.write("No configured demonstration thresholds were crossed.")

st.markdown("#### Explainable AI — Why was this flagged?")

if deviation_rows:
    st.warning(
        "The following readings differ significantly from the "
        "synthetic baseline."
    )

    st.dataframe(
        pd.DataFrame(deviation_rows),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success(
        "No individual readings exceeded the illustrative "
        "deviation threshold."
    )

st.caption(
    "Standard deviations describe differences from synthetic baseline data. "
    "They are not medical risk scores."
)


# =========================================================
# EARLY WARNING CENTER
# =========================================================

st.markdown("---")
st.markdown("""
<div class="section-heading">04 / EARLY WARNING CENTER</div>
<div class="section-sub">AUTOMATED SIMULATED HEALTH EVENT DETECTION</div>
""", unsafe_allow_html=True)

if alerts:
    for title, description in alerts:
        st.markdown(
            f"""
            <div class="alert-box">
                <div style="color:#ffbd68;font-weight:800;
                letter-spacing:1px;font-size:12px;">
                ⚠ {title}
                </div>
                <div style="color:#e8d8c6;font-size:13px;margin-top:7px;">
                {description}
                </div>
                <div style="color:#a58d77;font-size:10px;margin-top:8px;">
                SIMULATION ALERT • REVIEW REQUIRED
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.markdown("""
    <div class="safe-box">
        <div style="color:#62edc1;font-weight:800;">
        ✓ SYSTEM STATUS: NO CONFIGURED ALERTS
        </div>
        <div style="color:#9fcbbd;font-size:12px;margin-top:6px;">
        No demonstration alert conditions are currently active.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# HEALTH TREND ANALYTICS
# =========================================================

st.markdown("---")
st.markdown("""
<div class="section-heading">05 / HEALTH TREND ANALYTICS</div>
<div class="section-sub">24-HOUR SIMULATED TELEMETRY HISTORY</div>
""", unsafe_allow_html=True)


# Heart rate chart
fig_hr = go.Figure()

fig_hr.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Heart Rate"],
    mode="lines",
    name="Heart rate",
    line=dict(color="#42ddff", width=3),
    fill="tozeroy",
    fillcolor="rgba(66,221,255,0.07)"
))

fig_hr.add_hline(
    y=110,
    line_dash="dot",
    line_color="#ffad42",
    annotation_text="Illustrative alert threshold"
)

chart_layout(fig_hr, 290)
fig_hr.update_layout(title="♥ HEART RATE / BPM")


# Oxygen chart
fig_o2 = go.Figure()

fig_o2.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Oxygen Saturation"],
    mode="lines",
    name="Oxygen saturation",
    line=dict(color="#42e6b7", width=3),
    fill="tozeroy",
    fillcolor="rgba(66,230,183,0.07)"
))

fig_o2.add_hline(
    y=94,
    line_dash="dot",
    line_color="#ffad42",
    annotation_text="Illustrative alert threshold"
)

chart_layout(fig_o2, 290)
fig_o2.update_layout(title="◉ OXYGEN SATURATION / %")


# Temperature chart
fig_temp = go.Figure()

fig_temp.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Temperature"],
    mode="lines",
    name="Temperature",
    line=dict(color="#b08cff", width=3),
    fill="tozeroy",
    fillcolor="rgba(176,140,255,0.07)"
))

chart_layout(fig_temp, 290)
fig_temp.update_layout(title="⌁ BODY TEMPERATURE / °C")


# Radiation chart
fig_radiation = go.Figure()

fig_radiation.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Radiation Exposure Index"],
    mode="lines",
    name="Radiation exposure index",
    line=dict(color="#ffad42", width=3),
    fill="tozeroy",
    fillcolor="rgba(255,173,66,0.07)"
))

fig_radiation.add_hline(
    y=2.0,
    line_dash="dot",
    line_color="#ff7777",
    annotation_text="Illustrative demo threshold"
)

chart_layout(fig_radiation, 290)
fig_radiation.update_layout(title="☢ RADIATION EXPOSURE INDEX")


# Stress chart
fig_stress = go.Figure()

fig_stress.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Stress Indicator"],
    mode="lines",
    name="Stress indicator",
    line=dict(color="#d28cff", width=3),
    fill="tozeroy",
    fillcolor="rgba(210,140,255,0.07)"
))

fig_stress.add_hline(
    y=75,
    line_dash="dot",
    line_color="#ffad42",
    annotation_text="Illustrative demo threshold"
)

chart_layout(fig_stress, 290)
fig_stress.update_layout(title="🧠 STRESS INDICATOR / 100")


# Display charts
g1, g2 = st.columns(2)

with g1:
    st.plotly_chart(
        fig_hr,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with g2:
    st.plotly_chart(
        fig_o2,
        use_container_width=True,
        config={"displayModeBar": False}
    )

g3, g4 = st.columns(2)

with g3:
    st.plotly_chart(
        fig_temp,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with g4:
    st.plotly_chart(
        fig_radiation,
        use_container_width=True,
        config={"displayModeBar": False}
    )

st.plotly_chart(
    fig_stress,
    use_container_width=True,
    config={"displayModeBar": False}
)


# =========================================================
# SPACEFLIGHT HEALTH FACTORS
# =========================================================

st.markdown("---")
st.markdown("""
<div class="section-heading">06 / SPACEFLIGHT HEALTH FACTORS</div>
<div class="section-sub">ENVIRONMENTAL AND WELLBEING MONITORING</div>
""", unsafe_allow_html=True)

f1, f2 = st.columns(2)

with f1:
    st.markdown("#### ☢ Radiation exposure")

    st.metric(
        "SIMULATED EXPOSURE INDEX",
        f"{current_radiation:.2f}/5"
    )

    st.progress(
        min(current_radiation / 5, 1.0),
        text="Illustrative exposure index — not a real radiation dose"
    )

    st.markdown("#### 🧠 Stress indicator")

    st.metric(
        "SIMULATED INDICATOR",
        f"{current_stress:.0f}/100"
    )

    st.progress(
        current_stress / 100,
        text="Illustrative wellbeing indicator"
    )

    st.markdown("#### 🧍 Isolation indicator")

    st.metric(
        "SIMULATED INDICATOR",
        f"{current_isolation:.0f}/100"
    )

    st.progress(
        current_isolation / 100,
        text="Illustrative isolation indicator"
    )


with f2:
    st.markdown("#### 🦴 Bone health research indicator")

    st.metric(
        "SIMULATED BONE INDEX",
        f"{current_bone:.0f}/100"
    )

    st.progress(
        current_bone / 100,
        text="Illustrative placeholder — not a bone-density measurement"
    )

    st.markdown("#### 🏃 Physical activity")

    st.metric(
        "SIMULATED DAILY ACTIVITY",
        f"{current_activity:.0f} min"
    )

    st.progress(
        min(current_activity / 120, 1.0),
        text="Illustrative activity visualization"
    )

    st.markdown("#### 🌌 Microgravity exposure")

    st.metric(
        "SIMULATED INDICATOR",
        f"{current_microgravity:.0f}/100"
    )

    st.progress(
        current_microgravity / 100,
        text="Illustrative microgravity exposure indicator"
    )


st.info(
    "Research note: Immune-system changes are an important spaceflight health "
    "concern, but this prototype does not directly measure immune biomarkers. "
    "Immune monitoring could be added in a future version."
)


# =========================================================
# DATA EXPLORER
# =========================================================

st.markdown("---")
st.markdown("""
<div class="section-heading">07 / MISSION DATA EXPLORER</div>
<div class="section-sub">SIMULATED TELEMETRY RECORDS</div>
""", unsafe_allow_html=True)

with st.expander("OPEN TELEMETRY DATABASE"):

    st.dataframe(
        df.sort_values("Time", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ DOWNLOAD SIMULATED DATA CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="ASTRA_ORBIT01_SIMULATED_DATA.csv",
        mime="text/csv"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<div class="footer">
    <div style="font-family:Orbitron;color:#42ddff;
    font-size:19px;font-weight:800;letter-spacing:3px;">
    ASTRA HEALTH AI
    </div>
    <div style="margin-top:9px;">
    PROTECTING HUMAN HEALTH BEYOND EARTH
    </div>
    <div style="margin-top:12px;color:#496986;">
    STUDENT RESEARCH PROTOTYPE • ORBIT-01 • SIMULATED DATA ONLY
    </div>
</div>
""", unsafe_allow_html=True)
