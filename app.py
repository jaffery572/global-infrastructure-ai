import streamlit as st
import numpy as np

st.set_page_config(page_title="Global Infrastructure AI", layout="wide")

st.title("🏗️ Global Infrastructure AI Dashboard")
st.write("AI-powered infrastructure development predictor")

# Since model loading is failing, we'll use a demo function
def predict_infrastructure(population, area):
    """Demo prediction function"""
    # Simple calculation - replace with actual model when fixed
    score = (population / 1000) * 0.4 + (area / 100) * 0.3
    return min(score, 100)

# Inputs
st.sidebar.header("Input Parameters")
population = st.sidebar.slider("Population (thousands)", 0, 1000, 100, 10)
area = st.sidebar.slider("Area (sq km)", 0, 5000, 100, 50)

if st.button("🚀 Predict Infrastructure Need"):
    # Get prediction
    score = predict_infrastructure(population, area)
    
    # Display result
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Infrastructure Score", f"{score:.1f}/100")
    
    with col2:
        if score > 70:
            st.error("🚨 High Need")
        elif score > 40:
            st.warning("⚠️ Medium Need")
        else:
            st.success("✅ Low Need")
    
    # Recommendations
    st.subheader("Recommendations:")
    if score > 70:
        st.write("- Plan new roads and highways")
        st.write("- Upgrade water supply systems")
        st.write("- Invest in public transportation")
    elif score > 40:
        st.write("- Maintain existing infrastructure")
        st.write("- Plan for future expansion")
        st.write("- Improve connectivity")
    else:
        st.write("- Regular maintenance")
        st.write("- Monitor growth")
        st.write("- Technology upgrades")
    
    st.balloons()

st.info("Note: This is a demo version. Actual AI model integration in progress.")
