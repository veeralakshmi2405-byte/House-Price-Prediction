import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Load trained model
model = pickle.load(open("house_model.pkl", "rb"))

# Page config
st.set_page_config(page_title="House Price Prediction", page_icon="🏡", layout="wide")

# Header
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🏡 Smart House Price Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Enter the details of the house to get an instant price estimate 💰</p>", unsafe_allow_html=True)
st.write("---")

# Sidebar inputs
st.sidebar.header("🔧 Input House Details")

def user_input():
    bedrooms = st.sidebar.number_input("🛏 Bedrooms", 0, 20, 3)
    bathrooms = st.sidebar.number_input("🛁 Bathrooms", 0, 10, 2)
    sqft_living = st.sidebar.slider("📐 Living Area (sqft)", 500, 10000, 2000, step=50)
    sqft_lot = st.sidebar.slider("🌳 Lot Area (sqft)", 500, 50000, 5000, step=100)
    floors = st.sidebar.number_input("🏠 Floors", 1, 5, 1)
    waterfront = st.sidebar.selectbox("🌊 Waterfront View", [0, 1])
    view = st.sidebar.slider("👀 View Score", 0, 4, 0)
    condition = st.sidebar.slider("⚒ Condition", 1, 5, 3)
    grade = st.sidebar.slider("🏅 Grade", 1, 13, 7)
    sqft_above = st.sidebar.slider("⬆ Sqft Above", 400, 10000, 1500, step=50)
    sqft_basement = st.sidebar.slider("⬇ Sqft Basement", 0, 5000, 500, step=50)
    yr_built = st.sidebar.number_input("📅 Year Built", 1900, 2025, 2000)
    yr_renovated = st.sidebar.number_input("🔨 Year Renovated", 0, 2025, 0)
    zipcode = st.sidebar.number_input("📍 Zipcode", 98000, 99999, 98178)
    lat = st.sidebar.number_input("🌐 Latitude", value=47.5112, format="%.6f")
    long = st.sidebar.number_input("🌐 Longitude", value=-122.257, format="%.6f")
    sqft_living15 = st.sidebar.slider("📐 Living Area (15 neighbours)", 500, 10000, 2000, step=50)
    sqft_lot15 = st.sidebar.slider("🌳 Lot Area (15 neighbours)", 500, 50000, 5000, step=100)

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
    return pd.DataFrame([data])

df = user_input()

# Show inputs
st.subheader("📊 House Details You Entered")
st.dataframe(df, use_container_width=True)
st.write("---")

# Prediction
if st.button("🔮 Predict House Price"):
    prediction = model.predict(df)
    st.success(f"💰 Estimated House Price: **${prediction[0]:,.2f}**")
    st.balloons()

    # Visualization
    st.subheader("📈 Visualization")
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Bedrooms vs Price (dummy trend)
    sns.barplot(x=[df["bedrooms"][0]], y=[prediction[0]], ax=ax[0], color="skyblue")
    ax[0].set_title("Bedrooms vs Predicted Price")
    ax[0].set_xlabel("Bedrooms")
    ax[0].set_ylabel("Price")

    # Sqft vs Price (dummy trend)
    sns.scatterplot(x=[df["sqft_living"][0]], y=[prediction[0]], ax=ax[1], color="red", s=100)
    ax[1].set_title("Living Area vs Predicted Price")
    ax[1].set_xlabel("Living Area (sqft)")
    ax[1].set_ylabel("Price")

    st.pyplot(fig)

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; color: gray;">
        Developed with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
