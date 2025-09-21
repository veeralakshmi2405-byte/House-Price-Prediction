import streamlit as st
import pandas as pd
import pickle

# Load trained model
model = pickle.load(open("house_model.pkl", "rb"))

# App Config
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

# Sidebar Input
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
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Display input
st.markdown("### 🔎 Entered House Details")
st.dataframe(input_df.style.set_properties(**{'background-color': '#f9f9f9', 'color': '#000'}))

# Predict Button
if st.button("✨ Predict Price"):
    prediction = model.predict(input_df)
    st.markdown(
        f"""
        <div style="background-color:#2196F3;padding:20px;border-radius:10px;margin-top:20px;">
            <h2 style="color:white;text-align:center;">💰 Predicted House Price: ${prediction[0]:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
