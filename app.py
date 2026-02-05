import streamlit as st

st.title("🏗️ Global Infrastructure AI")
st.write("AI-powered infrastructure development predictor")

# Simple input
population = st.number_input("Population", value=100000)
area = st.number_input("Area (sq km)", value=100)

if st.button("Analyze"):
    # Simple calculation
    density = population / area
    
    if density > 500:
        st.error("High density - Development needed!")
    else:
        st.success("Adequate infrastructure!")
    
    st.metric("Density", f"{density:.1f} people/km²")
    st.balloons()

st.info("Model integration in progress. Live URL: https://global-infrastructure-ai-yqthyhbfx64ublu8nk72ik.streamlit.app")
