import streamlit as st
import pandas as pd
import joblib
import os

# ------------------------------
# Load trained model safely
# ------------------------------
model_path = "house_model.joblib"

if os.path.exists(model_path):
    model = joblib.load(model_path)
    st.success("✅ Model loaded successfully!")
else:
    st.error(f"❌ Error: {model_path} file illa!")
    st.stop()  # Stop app if model not found

# ------------------------------
# App Config
# ------------------------------
st.set_page_config(page_title="House Price Prediction", page_icon="🏡", layout="wide")

# Header Section
st.markdown(
    """
    <div style="background-color:#4CAF50;padding:20px;border-radius:10px;">
        <h1 style="color:white;text-align:center;">🏡 House Price Prediction App</h1>
        <p style="color:white;text-align:center;">Fill the details below to get an estimated house price instantly!</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ------------------------------
# Sidebar Input
# ------------------------------
st.sidebar.header("📌 Enter House Features")

def user_input_features():
    bedrooms = st.sidebar.number_input("Bedrooms", 1, 10, 3)
    bathrooms = st.sidebar.number_input("Bathrooms", 1, 10, 2)
    sqft_living = st.sidebar.number_input("Living Area (sqft)", 500, 10000, 2000)
    sqft_lot = st.sidebar.number_input("Lot Area (sqft)", 1000, 20000, 5000)
    floors = st.sidebar.number_input("Floors", 1, 4, 1)
    waterfront = st.sidebar.selectbox("Waterfront View", [0, 1])
    view = st.sidebar.slider("View Rating", 0, 4, 0)
    condition = st.sidebar.slider("Condition", 1, 5, 3)
    grade = st.sidebar.slider("Grade", 1, 13, 7)
    sqft_above = st.sidebar.number_input("Sqft Above", 500, 10000, 1800)
    sqft_basement = st.sidebar.number_input("Sqft Basement", 0, 5000, 200)
    yr_built = st.sidebar.number_input("Year Built", 1900, 2023, 2000)
    yr_renovated = st.sidebar.number_input("Year Renovated", 0, 2023, 0)

    # ✅ Extra features to match training data
    lat = st.sidebar.number_input("Latitude", 47.0, 48.0, 47.5)
    long = st.sidebar.number_input("Longitude", -123.0, -121.0, -122.0)
    sqft_living15 = st.sidebar.number_input("Living Area (15 Nearest)", 500, 6000, 2000)
    sqft_lot15 = st.sidebar.number_input("Lot Area (15 Nearest)", 500, 20000, 5000)
    zipcode = st.sidebar.number_input("Zipcode", 98000, 99999, 98103)

    data = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft_living": sqft_living,
        "sqft_lot": sqft_lot,
        "floors": floors,
        "waterfront": waterfront,
        "view": view,
        "condition": condition,
        "grade": grade,
        "sqft_above": sqft_above,
        "sqft_basement": sqft_basement,
        "yr_built": yr_built,
        "yr_renovated": yr_renovated,
        "zipcode": zipcode,
        "lat": lat,
        "long": long,
        "sqft_living15": sqft_living15,
        "sqft_lot15": sqft_lot15,
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# ✅ Reorder columns to match training model
feature_order = [
    'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
    'floors', 'waterfront', 'view', 'condition', 'grade',
    'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated',
    'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15'
]
input_df = input_df[feature_order]

# ------------------------------
# Display input
# ------------------------------
st.markdown("### 🔎 Entered House Details")
st.dataframe(input_df.style.set_properties(**{'background-color': '#f9f9f9', 'color': '#000'}))

# ------------------------------
# Predict Button
# ------------------------------
if st.button("✨ Predict Price"):
    try:
        prediction = model.predict(input_df)
        st.markdown(
            f"""
            <div style="background-color:#2196F3;padding:20px;border-radius:10px;margin-top:20px;">
                <h2 style="color:white;text-align:center;">💰 Predicted House Price: ${prediction[0]:,.2f}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Prediction error: {e}")
