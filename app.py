# ============================================
# 💎 PREMIUM INSURANCE COST PREDICTION APP
# ============================================

import streamlit as st
import pandas as pd
import joblib

# ============================================
# 🔥 FIX SKLEARN ERROR (_RemainderColsList)
# ============================================
import sklearn.compose._column_transformer as ct

if not hasattr(ct, "_RemainderColsList"):
    class _RemainderColsList(list):
        pass
    ct._RemainderColsList = _RemainderColsList

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Insurance Predictor",
    page_icon="💰",
    layout="wide"
)

# ============================================
# 💎 PREMIUM CSS DESIGN
# ============================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main {
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
}

h1 {
    text-align: center;
    color: #00ffe1;
    font-size: 45px;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #cccccc;
    margin-bottom: 30px;
}

.stButton>button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    font-size: 18px;
    background: linear-gradient(45deg, #00ffe1, #007cf0);
    color: black;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px #00ffe1;
}

.result-box {
    background: linear-gradient(45deg, #00ffe1, #00c6ff);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: black;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# TITLE
# ============================================
st.markdown("<h1>💰 Insurance Cost Prediction</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered smart insurance estimator</div>", unsafe_allow_html=True)

# ============================================
# LOAD MODEL
# ============================================
@st.cache_resource
def load_model():
    try:
        return joblib.load("model.pkl")
    except Exception as e:
        st.error(f"❌ Model Loading Failed: {e}")
        st.stop()

model = load_model()

# ============================================
# INPUT UI
# ============================================
col1, col2 = st.columns(2)

with col1:
    age = st.slider("🎂 Age", 18, 100, 25)
    bmi = st.slider("⚖️ BMI", 10.0, 50.0, 25.0)
    children = st.slider("👶 Children", 0, 5, 0)

with col2:
    sex = st.selectbox("🧑 Sex", ["male", "female"])
    smoker = st.selectbox("🚬 Smoker", ["yes", "no"])
    region = st.selectbox("🌍 Region", ["southwest", "southeast", "northwest", "northeast"])

# ============================================
# PREDICTION BUTTON
# ============================================
if st.button("🚀 Predict Insurance Cost"):

    try:
        # ✅ RAW INPUT (Pipeline Model)
        input_df = pd.DataFrame({
            "age": [age],
            "sex": [sex],
            "bmi": [bmi],
            "children": [children],
            "smoker": [smoker],
            "region": [region]
        })

        with st.spinner("🔮 Analyzing your data..."):
            prediction = model.predict(input_df)[0]

        # ============================================
        # RESULT DISPLAY
        # ============================================
        st.markdown(
            f"<div class='result-box'>💰 Estimated Cost: ₹ {prediction:,.2f}</div>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")
