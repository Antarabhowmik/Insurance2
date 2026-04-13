# ================================
# 🚀 INSURANCE COST PREDICTION APP
# ================================

import streamlit as st
import pandas as pd
import joblib

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Insurance Predictor",
    page_icon="💰",
    layout="wide"
)

# ================================
# LOAD MODEL
# ================================
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# ================================
# CUSTOM CSS + HTML (ULTRA PREMIUM)
# ================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

/* ── Root Variables ── */
:root {
  --void:       #05060a;
  --deep:       #090c14;
  --surface:    #0d1120;
  --glass:      rgba(255,255,255,0.04);
  --glass-h:    rgba(255,255,255,0.07);
  --cyan:       #00e5ff;
  --violet:     #7c3aed;
  --gold:       #f59e0b;
  --glow-c:     rgba(0,229,255,0.28);
  --glow-v:     rgba(124,58,237,0.28);
  --text-1:     #f0f4ff;
  --text-2:     #8a93b0;
  --text-3:     #4a5270;
  --border:     rgba(255,255,255,0.06);
  --border-a:   rgba(0,229,255,0.2);
  --r-md:       14px;
  --r-lg:       22px;
  --r-xl:       32px;
  --ff-disp:    'Syne', sans-serif;
  --ff-body:    'Instrument Sans', sans-serif;
  --ff-mono:    'DM Mono', monospace;
}

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
  background: var(--void) !important;
  font-family: var(--ff-body) !important;
  color: var(--text-1) !important;
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Animated nebula background ── */
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(124,58,237,0.13) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,229,255,0.09) 0%, transparent 55%),
    radial-gradient(ellipse 40% 60% at 60% 30%, rgba(245,158,11,0.05) 0%, transparent 50%);
  pointer-events: none; z-index: 0;
  animation: nebula 20s ease-in-out infinite alternate;
}
@keyframes nebula {
  0%   { opacity:.7; transform:scale(1) translateY(0); }
  100% { opacity:1;  transform:scale(1.04) translateY(-12px); }
}

/* Scanline texture */
.stApp::after {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(0,0,0,0.04) 2px, rgba(0,0,0,0.04) 4px
  );
  pointer-events: none; z-index: 1;
}

/* ── Layout ── */
.main .block-container {
  max-width: 980px !important;
  padding: 2.5rem 2rem !important;
  position: relative; z-index: 2;
}

/* ── Columns as glass cards ── */
[data-testid="column"] {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-lg) !important;
  padding: 1.8rem 2rem !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  transition: border-color .3s, background .3s;
  animation: cardIn .65s cubic-bezier(.16,1,.3,1) both;
}
[data-testid="column"]:nth-child(1) { animation-delay:.15s; }
[data-testid="column"]:nth-child(2) { animation-delay:.3s; }
[data-testid="column"]:hover {
  background: var(--glass-h) !important;
  border-color: var(--border-a) !important;
}
@keyframes cardIn {
  from { opacity:0; transform:translateY(28px); }
  to   { opacity:1; transform:translateY(0); }
}
[data-testid="stHorizontalBlock"] { gap: 1.2rem !important; align-items: start !important; }

/* ── Labels ── */
label, .stSlider label, .stSelectbox label {
  font-family: var(--ff-mono) !important;
  font-size: 11px !important; font-weight: 500 !important;
  letter-spacing: .12em !important; text-transform: uppercase !important;
  color: var(--text-2) !important; margin-bottom: 6px !important;
}

/* ── Sliders ── */
.stSlider > div > div > div {
  height: 4px !important; border-radius: 99px !important;
  background: rgba(255,255,255,0.08) !important;
}
.stSlider [data-baseweb="slider"] [role="progressbar"] {
  background: linear-gradient(90deg, var(--violet), var(--cyan)) !important;
  border-radius: 99px !important;
}
.stSlider [data-baseweb="slider"] [role="slider"] {
  width: 20px !important; height: 20px !important;
  border-radius: 50% !important; background: var(--void) !important;
  border: 2px solid var(--cyan) !important;
  box-shadow: 0 0 14px var(--glow-c), 0 0 0 4px rgba(0,229,255,.08) !important;
  cursor: grab !important;
  transition: box-shadow .2s, transform .2s !important;
}
.stSlider [data-baseweb="slider"] [role="slider"]:hover {
  transform: scale(1.28) !important;
  box-shadow: 0 0 24px var(--glow-c), 0 0 0 6px rgba(0,229,255,.15) !important;
}
.stSlider [data-baseweb="slider"] [role="slider"]:active { cursor: grabbing !important; }
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] {
  font-family: var(--ff-mono) !important;
  font-size: 11px !important; color: var(--text-3) !important;
}

/* ── Selectboxes ── */
.stSelectbox > div > div {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important;
  color: var(--text-1) !important;
  font-family: var(--ff-body) !important;
  font-size: 15px !important;
  transition: border-color .25s, box-shadow .25s, background .25s !important;
  backdrop-filter: blur(8px) !important;
}
.stSelectbox > div > div:hover {
  background: rgba(255,255,255,0.09) !important;
  border-color: rgba(0,229,255,.35) !important;
  box-shadow: 0 0 0 3px rgba(0,229,255,.1) !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 3px rgba(0,229,255,.15) !important;
}
.stSelectbox svg { color: var(--cyan) !important; fill: var(--cyan) !important; }
[data-baseweb="popover"] ul, [data-baseweb="menu"] {
  background: #111827 !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important;
  backdrop-filter: blur(20px) !important;
  box-shadow: 0 20px 60px rgba(0,0,0,.6) !important;
}
[data-baseweb="menu"] li {
  color: var(--text-2) !important;
  font-family: var(--ff-body) !important;
  font-size: 14px !important;
  transition: background .15s, color .15s !important;
}
[data-baseweb="menu"] li:hover, [data-baseweb="menu"] li[aria-selected="true"] {
  background: rgba(0,229,255,.08) !important; color: var(--cyan) !important;
}

/* ── Predict Button ── */
.stButton > button {
  width: 100% !important; padding: 1rem 2rem !important;
  font-family: var(--ff-disp) !important;
  font-size: 16px !important; font-weight: 700 !important;
  letter-spacing: .08em !important; text-transform: uppercase !important;
  color: #050a14 !important;
  background: linear-gradient(135deg, var(--cyan) 0%, #009abb 45%, var(--violet) 100%) !important;
  background-size: 200% 200% !important;
  border: none !important; border-radius: var(--r-md) !important;
  cursor: pointer !important; position: relative !important; overflow: hidden !important;
  transition: transform .2s cubic-bezier(.34,1.56,.64,1), box-shadow .3s !important;
  box-shadow: 0 4px 28px var(--glow-c), 0 2px 8px rgba(0,0,0,.4) !important;
  animation: bgShift 4s ease infinite, btnIn .5s .5s cubic-bezier(.16,1,.3,1) both !important;
}
@keyframes bgShift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes btnIn {
  from { opacity:0; transform:translateY(10px); }
  to   { opacity:1; transform:translateY(0); }
}
.stButton > button::before {
  content: '';
  position: absolute; top:0; left:-100%;
  width:100%; height:100%;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,.28) 50%, transparent 100%);
  transition: left .5s ease;
}
.stButton > button:hover::before { left:100%; }
.stButton > button:hover {
  transform: translateY(-3px) scale(1.015) !important;
  box-shadow: 0 10px 44px var(--glow-c), 0 4px 16px rgba(0,0,0,.5) !important;
}
.stButton > button:active {
  transform: translateY(0) scale(.98) !important;
  box-shadow: 0 2px 12px var(--glow-c) !important;
}
.stButton > button::after {
  content: '';
  position: absolute; inset:-1px;
  border-radius: inherit;
  border: 1px solid rgba(0,229,255,.5);
  animation: pulseRing 2.5s ease-out infinite;
  pointer-events: none;
}
@keyframes pulseRing {
  0%   { opacity:1; transform:scale(1); }
  70%  { opacity:0; transform:scale(1.07); }
  100% { opacity:0; transform:scale(1.07); }
}

/* ── Result Box ── */
.result-box {
  position: relative !important; overflow: hidden !important;
  background: var(--surface) !important;
  border: 1px solid rgba(0,229,255,.22) !important;
  border-radius: var(--r-lg) !important;
  padding: 2.8rem 2rem !important;
  text-align: center !important;
  box-shadow: 0 0 0 1px rgba(0,229,255,.1), 0 0 50px rgba(0,229,255,.13), 0 24px 64px rgba(0,0,0,.55) !important;
  animation: resultReveal .65s cubic-bezier(.16,1,.3,1) both !important;
  backdrop-filter: blur(14px) !important;
  -webkit-backdrop-filter: blur(14px) !important;
}
@keyframes resultReveal {
  from { opacity:0; transform:scale(.9) translateY(22px); }
  to   { opacity:1; transform:scale(1) translateY(0); }
}
.result-box::before {
  content: '';
  position: absolute; top:-60%; left:-60%;
  width:220%; height:220%;
  background: conic-gradient(
    from 0deg, transparent 0deg,
    rgba(0,229,255,.06) 60deg, transparent 120deg,
    rgba(124,58,237,.06) 240deg, transparent 300deg
  );
  animation: coneRot 8s linear infinite;
  pointer-events: none;
}
@keyframes coneRot { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
.result-box::after {
  content: '';
  position: absolute; top:0; left:10%; right:10%;
  height:2px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
  border-radius: 99px;
}

/* ── Alerts ── */
.stAlert {
  background: rgba(239,68,68,.08) !important;
  border: 1px solid rgba(239,68,68,.25) !important;
  border-radius: var(--r-md) !important;
  color: #fca5a5 !important;
  font-family: var(--ff-mono) !important;
  font-size: 13px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--deep); }
::-webkit-scrollbar-thumb { background: var(--violet); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan); }

/* ── Spacing ── */
.element-container { margin-bottom: 1.1rem !important; }
hr { border:none !important; height:1px !important;
     background:linear-gradient(90deg,transparent,var(--border),transparent) !important;
     margin:1.5rem 0 !important; }

/* ── Hide Streamlit chrome ── */
footer, #MainMenu, header[data-testid="stHeader"] {
  visibility: hidden !important; height: 0 !important;
}

/* ── Floating orbs (decorative) ── */
.main .block-container::before {
  content: '';
  position: fixed; top:12%; right:6%;
  width:200px; height:200px;
  border-radius: 50%;
  border: 1px solid rgba(0,229,255,.05);
  animation: floatOrb 14s ease-in-out infinite;
  pointer-events: none; z-index: 0;
}
.main .block-container::after {
  content: '';
  position: fixed; bottom:18%; left:4%;
  width:130px; height:130px;
  border-radius: 50%;
  border: 1px solid rgba(124,58,237,.07);
  animation: floatOrb 18s ease-in-out infinite reverse;
  pointer-events: none; z-index: 0;
}
@keyframes floatOrb {
  0%,100% { transform:translateY(0) scale(1); opacity:.5; }
  50%      { transform:translateY(-28px) scale(1.06); opacity:1; }
}

/* ── Responsive ── */
@media (max-width:640px) {
  .main .block-container { padding:1.4rem 1rem !important; }
  [data-testid="stHorizontalBlock"] { flex-direction:column !important; gap:1rem !important; }
  [data-testid="column"] { padding:1.2rem !important; }
}

/* ── Keyframe: fadeUp (used by hero HTML below) ── */
@keyframes fadeUp {
  from { opacity:0; transform:translateY(18px); }
  to   { opacity:1; transform:translateY(0); }
}
</style>

<!-- ══════════════════════════════════
     HERO HEADER
     ══════════════════════════════════ -->
<div style="
  text-align: center;
  padding: 2.4rem 1rem 2rem;
  position: relative;
  z-index: 2;
">

  <!-- Eyebrow pill -->
  <div style="
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: #00e5ff;
    background: rgba(0,229,255,.07);
    border: 1px solid rgba(0,229,255,.18);
    border-radius: 99px;
    padding: 5px 18px;
    margin-bottom: 1.2rem;
    animation: fadeUp .5s cubic-bezier(.16,1,.3,1) both;
  ">
    <span style="
      width:6px; height:6px;
      background:#00e5ff;
      border-radius:50%;
      box-shadow:0 0 8px rgba(0,229,255,.8);
      display:inline-block;
      animation: blink 2s ease-in-out infinite;
    "></span>
    AI-Powered · Real-Time Estimate
  </div>

  <!-- Main title -->
  <div style="
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 3.6rem);
    font-weight: 800;
    letter-spacing: -.03em;
    line-height: 1.06;
    background: linear-gradient(135deg, #ffffff 0%, #00e5ff 48%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 36px rgba(0,229,255,.28));
    animation: fadeUp .6s .1s cubic-bezier(.16,1,.3,1) both;
    margin-bottom: .7rem;
  ">Insurance Cost<br>Predictor</div>

  <!-- Subtitle -->
  <p style="
    font-family: 'Instrument Sans', sans-serif;
    font-size: 15px;
    color: #8a93b0;
    max-width: 420px;
    margin: 0 auto 1.6rem;
    line-height: 1.65;
    animation: fadeUp .6s .2s cubic-bezier(.16,1,.3,1) both;
  ">Enter your details below to instantly estimate your annual health insurance premium using our trained ML model</p>

  <!-- Decorative separator line -->
  <div style="
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    animation: fadeUp .6s .3s cubic-bezier(.16,1,.3,1) both;
  ">
    <div style="width:32px;height:1px;background:rgba(255,255,255,.1);"></div>
    <div style="width:8px;height:8px;border:1px solid rgba(0,229,255,.3);border-radius:2px;transform:rotate(45deg);"></div>
    <div style="width:32px;height:1px;background:rgba(255,255,255,.1);"></div>
  </div>

</div>

<!-- ══════════════════════════════════
     SECTION LABEL
     ══════════════════════════════════ -->
<div style="
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: #4a5270;
  margin-bottom: .8rem;
  padding-left: 4px;
  position: relative; z-index: 2;
">// Input Parameters</div>

<style>
@keyframes blink {
  0%,100% { opacity:1; }
  50%      { opacity:.3; }
}
</style>
""", unsafe_allow_html=True)

# ================================
# INPUT SECTION
# ================================
col1, col2 = st.columns(2)

with col1:
    age      = st.slider("Age", 18, 100, 25)
    bmi      = st.slider("BMI", 10.0, 50.0, 25.0)
    children = st.slider("Children", 0, 5, 0)

with col2:
    sex    = st.selectbox("Sex", ["male", "female"])
    smoker = st.selectbox("Smoker", ["yes", "no"])
    region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

# Spacer
st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

# ================================
# PREDICT BUTTON + RESULT
# ================================
if st.button("⚡  Predict My Insurance Cost"):

    input_df = pd.DataFrame({
        "age":      [age],
        "sex":      [sex],
        "bmi":      [bmi],
        "children": [children],
        "smoker":   [smoker],
        "region":   [region]
    })

    try:
        prediction = model.predict(input_df)[0]

        st.markdown(
            f"""
            <div class="result-box">

              <!-- Top label -->
              <div style="
                font-family:'DM Mono',monospace;
                font-size:10px;
                letter-spacing:.2em;
                text-transform:uppercase;
                color:#4a5270;
                margin-bottom:.5rem;
              ">// Estimated Annual Premium</div>

              <!-- Amount -->
              <div style="
                font-family:'Syne',sans-serif;
                font-size:clamp(2rem,5vw,3.2rem);
                font-weight:800;
                color:#00e5ff;
                text-shadow: 0 0 32px rgba(0,229,255,.5);
                letter-spacing:-.02em;
                line-height:1.1;
              ">₹ {prediction:,.2f}</div>

              <!-- Divider -->
              <div style="
                width:40px; height:1px;
                background:rgba(0,229,255,.25);
                margin:1rem auto;
                border-radius:99px;
              "></div>

              <!-- Meta row -->
              <div style="
                display:flex;
                justify-content:center;
                gap:1.4rem;
                flex-wrap:wrap;
              ">
                <span style="
                  font-family:'DM Mono',monospace;
                  font-size:11px;
                  color:#4a5270;
                  display:flex; align-items:center; gap:5px;
                ">
                  <span style="width:5px;height:5px;background:#00e5ff;border-radius:50%;opacity:.6;"></span>
                  Age {age}
                </span>
                <span style="
                  font-family:'DM Mono',monospace;
                  font-size:11px;
                  color:#4a5270;
                  display:flex; align-items:center; gap:5px;
                ">
                  <span style="width:5px;height:5px;background:#7c3aed;border-radius:50%;opacity:.6;"></span>
                  BMI {bmi:.1f}
                </span>
                <span style="
                  font-family:'DM Mono',monospace;
                  font-size:11px;
                  color:#4a5270;
                  display:flex; align-items:center; gap:5px;
                ">
                  <span style="width:5px;height:5px;background:#f59e0b;border-radius:50%;opacity:.6;"></span>
                  Smoker: {smoker}
                </span>
                <span style="
                  font-family:'DM Mono',monospace;
                  font-size:11px;
                  color:#4a5270;
                  display:flex; align-items:center; gap:5px;
                ">
                  <span style="width:5px;height:5px;background:#10b981;border-radius:50%;opacity:.6;"></span>
                  {region.title()}
                </span>
              </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Prediction error: {e}")
