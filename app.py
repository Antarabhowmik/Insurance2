# ================================
# 🚀 INSURANCE COST PREDICTION APP
# ================================

import streamlit as st
import pandas as pd
import joblib
import sys

# ================================
# 🔥 FORCE SKLEARN COMPATIBILITY PATCH
# ================================
try:
    import sklearn
    import sklearn.compose._column_transformer as ct

    # Fix missing internal class (_RemainderColsList)
    if not hasattr(ct, "_RemainderColsList"):
        class _RemainderColsList(list):
            pass
        ct._RemainderColsList = _RemainderColsList

except Exception as e:
    print("Patch warning:", e)

# ================================
# IMPORTANT IMPORTS (REQUIRED FOR MODEL)
# ================================
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Insurance Predictor",
    page_icon="💰",
    layout="centered"
)

# ================================
# UI
# ================================
st.title("💰 Insurance Cost Prediction")
st.caption("Smart ML-based Insurance Price Estimator")

# ================================
# LOAD MODEL (SAFE + FALLBACK)
# ================================
@st.cache_resource
def load_model():
    try:
        model = joblib.load("model.pkl")
        return model

    except Exception as e:
        st.warning("⚠️ Model load failed, using fallback logic")
        st.error(f"Error: {e}")

        # 🔥 FALLBACK MODEL (MANUAL LOGIC)
        def fallback_predict(df):
            # simple approximation formula
            base = 2000
            age_factor = df["age"].values[0] * 50
            bmi_factor = df["bmi"].values[0] * 100
            child_factor = df["children"].values[0] * 500
            smoker_factor = 20000 if df["smoker"].values[0] == "yes" else 0

            return [base + age_factor + bmi_factor + child_factor + smoker_factor]

        return fallback_predict

model = load_model()

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
# PREDICTION
# ================================
if st.button("🚀 Predict Insurance Cost"):

    input_df = pd.DataFrame({
        "age": [age],
        "sex": [sex],
        "bmi": [bmi],
        "children": [children],
        "smoker": [smoker],
        "region": [region]
    })

    try:
        # If real model
        if hasattr(model, "predict"):
            prediction = model.predict(input_df)[0]
        else:
            # fallback function
            prediction = model(input_df)[0]

        st.success(f"💰 Estimated Cost: ₹ {prediction:,.2f}")

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")
