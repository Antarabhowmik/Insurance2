# ============================================
# 💎 PREMIUM INSURANCE COST PREDICTION APP
# ============================================

import streamlit as st
import pandas as pd
import joblib

# ============================================
# FIX SKLEARN ERROR
# ============================================
import sklearn.compose._column_transformer as ct

if not hasattr(ct, "_RemainderColsList"):
    class _RemainderColsList(list):
        pass
    ct._RemainderColsList = _RemainderColsList

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="Insurance Predictor", page_icon="💰", layout="wide")

# ============================================
# PREMIUM UI
# ============================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
h1 {
    text-align: center;
    color: #00ffe1;
}
.stButton>button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    background: linear-gradient(45deg, #00ffe1, #007cf0);
}
.result-box {
    background: linear-gradient(45deg, #00ffe1, #00c6ff);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 28px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💰 Insurance Cost Prediction</h1>", unsafe_allow_html=True)

# ============================================
# LOAD MODEL
# ============================================
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# ============================================
# INPUTS
# ============================================
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 100, 25)
    bmi = st.slider("BMI", 10.0, 50.0, 25.0)
    children = st.slider("Children", 0, 5, 0)

with col2:
    sex = st.selectbox("Sex", ["male", "female"])
    smoker = st.selectbox("Smoker", ["yes", "no"])
    region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

# ============================================
# PREDICTION
# ============================================
if st.button("🚀 Predict Insurance Cost"):

    try:
        # 🔥 EXACT 11 FEATURES (MATCH MODEL)
        input_data = {
            "age": age,
            "bmi": bmi,
            "children": children,

            # Sex (drop one to avoid dummy trap)
            "sex_male": 1 if sex == "male" else 0,

            # Smoker
            "smoker_yes": 1 if smoker == "yes" else 0,

            # Region (3 columns if one dropped during training)
            "region_northwest": 1 if region == "northwest" else 0,
            "region_southeast": 1 if region == "southeast" else 0,
            "region_southwest": 1 if region == "southwest" else 0,
        }

        # ⚠️ IMPORTANT: Fill missing columns
        expected_cols = [
            "age", "bmi", "children",
            "sex_male",
            "smoker_yes",
            "region_northwest", "region_southeast", "region_southwest"
        ]

        input_df = pd.DataFrame([input_data])

        # Add missing columns with 0
        for col in expected_cols:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[expected_cols]

        prediction = model.predict(input_df)[0]

        st.markdown(
            f"<div class='result-box'>💰 Estimated Cost: ₹ {prediction:,.2f}</div>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")
