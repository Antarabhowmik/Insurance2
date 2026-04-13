# =========================================================
# 💎 INSURANCE COST PREDICTION (FINAL PRODUCTION APP)
# =========================================================

import streamlit as st
import pandas as pd
import joblib

# =========================================================
# 🔧 SKLEARN COMPATIBILITY PATCH
# =========================================================
import sklearn.compose._column_transformer as ct
if not hasattr(ct, "_RemainderColsList"):
    class _RemainderColsList(list):
        pass
    ct._RemainderColsList = _RemainderColsList

# =========================================================
# ⚙️ PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Insurance AI Predictor",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# 🎨 PREMIUM UI (INLINE CSS)
# =========================================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#00ffe1;
}
.subtitle {
    text-align:center;
    color:#ccc;
    margin-bottom:30px;
}
.stButton>button {
    width:100%;
    height:60px;
    border-radius:15px;
    font-size:18px;
    background: linear-gradient(45deg,#00ffe1,#007cf0);
    color:black;
    border:none;
    transition:0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow:0 0 20px #00ffe1;
}
.result-box {
    background: linear-gradient(45deg,#00ffe1,#00c6ff);
    padding:25px;
    border-radius:15px;
    text-align:center;
    font-size:28px;
    font-weight:bold;
    color:black;
    margin-top:25px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 🧾 HEADER
# =========================================================
st.markdown("<div class='title'>💰 Insurance Cost Prediction</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered premium prediction system</div>", unsafe_allow_html=True)

# =========================================================
# 📦 LOAD MODEL
# =========================================================
@st.cache_resource
def load_model():
    try:
        return joblib.load("model.pkl")
    except Exception as e:
        st.error(f"❌ Model Loading Failed: {e}")
        st.stop()

model = load_model()

# =========================================================
# 📊 INPUT UI
# =========================================================
col1, col2 = st.columns(2)

with col1:
    age = st.slider("🎂 Age", 18, 100, 25)
    bmi = st.slider("⚖️ BMI", 10.0, 50.0, 25.0)
    children = st.slider("👶 Children", 0, 5, 0)

with col2:
    sex = st.selectbox("🧑 Sex", ["male", "female"])
    smoker = st.selectbox("🚬 Smoker", ["yes", "no"])
    region = st.selectbox("🌍 Region", ["southwest", "southeast", "northwest", "northeast"])

# =========================================================
# 🔮 PREDICTION
# =========================================================
if st.button("🚀 Predict Insurance Cost"):

    try:
        # 🔥 PURE NUMERIC INPUT (MATCH MODEL)
        input_data = {
            "age": age,
            "bmi": bmi,
            "children": children,

            # Encoding
            "sex_male": 1 if sex == "male" else 0,
            "smoker_yes": 1 if smoker == "yes" else 0,

            "region_northeast": 1 if region == "northeast" else 0,
            "region_northwest": 1 if region == "northwest" else 0,
            "region_southeast": 1 if region == "southeast" else 0,
            "region_southwest": 1 if region == "southwest" else 0,
        }

        input_df = pd.DataFrame([input_data])

        # 🔥 MATCH EXACT MODEL FEATURES
        if hasattr(model, "feature_names_in_"):
            input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)

        # Prediction
        with st.spinner("🔮 AI is analyzing..."):
            prediction = model.predict(input_df)[0]

        # Display Result
        st.markdown(
            f"<div class='result-box'>💰 Estimated Cost: ₹ {prediction:,.2f}</div>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")
