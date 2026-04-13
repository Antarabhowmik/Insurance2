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
# LOAD MODEL (FAST & CACHED)
# ================================
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

# ================================
# CUSTOM CSS (PREMIUM FUTURISTIC UI)
# ================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.main {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
}
h1 {
    text-align: center;
    color: #00ffe1;
    font-size: 40px;
}
.stButton>button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    font-size: 18px;
    background: linear-gradient(45deg, #00ffe1, #007cf0);
    color: black;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
}
.result-box {
    background: linear-gradient(45deg, #00ffe1, #00c6ff);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: black;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# TITLE
# ================================
st.markdown("<h1>💰 Insurance Cost Prediction</h1>", unsafe_allow_html=True)

# ================================
# INPUT SECTION
# ================================
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 100, 25)
    bmi = st.slider("BMI", 10.0, 50.0, 25.0)
    children = st.slider("Children", 0, 5, 0)

with col2:
    sex = st.selectbox("Sex", ["male", "female"])
    smoker = st.selectbox("Smoker", ["yes", "no"])
    region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

# ================================
# PREDICTION BUTTON
# ================================
if st.button("🚀 Predict Insurance Cost"):

    # Load model only when needed (faster startup)
    model = load_model()

    # Input validation
    if bmi <= 0:
        st.error("❌ BMI must be positive")
    else:
        # Create DataFrame (IMPORTANT FIX)
        input_df = pd.DataFrame({
            "age": [age],
            "sex": [sex],
            "bmi": [bmi],
            "children": [children],
            "smoker": [smoker],
            "region": [region]
        })

        try:
            # Loading animation
            with st.spinner("🔮 Predicting... Please wait"):
                prediction = model.predict(input_df)[0]

            # Show result
            st.markdown(
                f'<div class="result-box">💰 Estimated Cost: ₹ {prediction:,.2f}</div>',
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
