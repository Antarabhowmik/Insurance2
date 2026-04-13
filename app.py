# ============================================
# 💎 FINAL FIXED INSURANCE APP (NO ERROR)
# ============================================

import streamlit as st
import pandas as pd
import joblib

# ================================
# FIX SKLEARN ERROR
# ================================
import sklearn.compose._column_transformer as ct

if not hasattr(ct, "_RemainderColsList"):
    class _RemainderColsList(list):
        pass
    ct._RemainderColsList = _RemainderColsList

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(page_title="Insurance Predictor", page_icon="💰", layout="wide")

# ================================
# UI
# ================================
st.markdown("<h1 style='text-align:center;color:#00ffe1;'>💰 Insurance Cost Prediction</h1>", unsafe_allow_html=True)

# ================================
# LOAD MODEL
# ================================
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# ================================
# INPUTS
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
# PREDICTION
# ================================
if st.button("🚀 Predict Insurance Cost"):

    try:
        # 🔥 INCLUDE BOTH RAW + ENCODED (FINAL FIX)
        input_data = {
            # ORIGINAL FEATURES
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region,

            # ENCODED FEATURES
            "sex_male": 1 if sex == "male" else 0,
            "sex_female": 1 if sex == "female" else 0,

            "smoker_yes": 1 if smoker == "yes" else 0,
            "smoker_no": 1 if smoker == "no" else 0,

            "region_northeast": 1 if region == "northeast" else 0,
            "region_northwest": 1 if region == "northwest" else 0,
            "region_southeast": 1 if region == "southeast" else 0,
            "region_southwest": 1 if region == "southwest" else 0,
        }

        input_df = pd.DataFrame([input_data])

        prediction = model.predict(input_df)[0]

        st.success(f"💰 Estimated Cost: ₹ {prediction:,.2f}")

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")
