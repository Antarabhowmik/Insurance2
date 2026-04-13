# ============================================
# 💎 FINAL UNIVERSAL INSURANCE APP (NO ERRORS)
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
    try:
        return joblib.load("model.pkl")
    except Exception as e:
        st.error(f"❌ Model Loading Failed: {e}")
        st.stop()

model = load_model()

# ============================================
# DEBUG (SEE MODEL FEATURES)
# ============================================
if hasattr(model, "feature_names_in_"):
    st.write("🔍 Model expects features:")
    st.write(model.feature_names_in_)

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
        # 🔥 CREATE EMPTY INPUT WITH EXACT MODEL FEATURES
        if hasattr(model, "feature_names_in_"):
            input_df = pd.DataFrame(columns=model.feature_names_in_)
        else:
            st.error("❌ Model has no feature_names_in_ attribute")
            st.stop()

        # Initialize all to 0
        input_df.loc[0] = 0

        # ============================================
        # FILL NUMERICAL
        # ============================================
        for col in ["age", "bmi", "children"]:
            if col in input_df.columns:
                input_df[col] = locals()[col]

        # ============================================
        # HANDLE CATEGORICAL
        # ============================================

        # RAW columns
        if "sex" in input_df.columns:
            input_df["sex"] = sex

        if "smoker" in input_df.columns:
            input_df["smoker"] = smoker

        if "region" in input_df.columns:
            input_df["region"] = region

        # ENCODED columns
        for col in input_df.columns:

            # sex encoding
            if col.startswith("sex_"):
                input_df[col] = 1 if col == f"sex_{sex}" else 0

            # smoker encoding
            if col.startswith("smoker_"):
                input_df[col] = 1 if col == f"smoker_{smoker}" else 0

            # region encoding
            if col.startswith("region_"):
                input_df[col] = 1 if col == f"region_{region}" else 0

        # ============================================
        # PREDICT
        # ============================================
        prediction = model.predict(input_df)[0]

        st.markdown(
            f"<div class='result-box'>💰 Estimated Cost: ₹ {prediction:,.2f}</div>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")
