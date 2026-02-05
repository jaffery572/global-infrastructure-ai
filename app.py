import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="AI Model Predictor",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 AI Model Prediction Dashboard")
st.markdown("### Random Forest Classifier - Live Predictions")

# Load model
@st.cache_resource
def load_model():
    try:
        with open('ai_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None

model = load_model()

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    # Model info
    if model:
        st.success("✅ Model Loaded")
        st.info(f"**Model Type:** RandomForestClassifier")
        st.info(f"**Trees:** {model.n_estimators}")
        st.info(f"**Classes:** {len(model.classes_)}")
    
    st.markdown("---")
    st.caption("Global Infrastructure AI Project")

# Main content
if model:
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Input Features")
        age = st.slider("Age", 18, 100, 35, 1)
        budget = st.number_input("Budget ($)", 1000, 1000000, 50000, 1000)
    
    with col2:
        st.subheader("📈 Feature Importance")
        if hasattr(model, 'feature_importances_'):
            features = ['age', 'budget']
            importance = model.feature_importances_
            
            fig = go.Figure(data=[
                go.Bar(x=features, y=importance)
            ])
            fig.update_layout(
                title="Feature Importance",
                yaxis_title="Importance Score",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Predict button
    st.markdown("---")
    predict_btn = st.button("🚀 PREDICT NOW", type="primary", use_container_width=True)
    
    if predict_btn:
        # Create input array
        input_data = np.array([[age, budget]])
        
        # Get predictions
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        # Results
        st.subheader("🎯 Prediction Results")
        
        # Result cards
        cols = st.columns(3)
        with cols[0]:
            st.metric("Predicted Class", f"Class {prediction}")
        
        with cols[1]:
            confidence = max(probabilities) * 100
            st.metric("Confidence", f"{confidence:.1f}%")
        
        with cols[2]:
            st.metric("Input Features", "2")
        
        # Probability chart
        st.subheader("📊 Probability Distribution")
        
        fig2 = make_subplots(rows=1, cols=2, 
                            subplot_titles=("Probability Bar Chart", "Donut Chart"))
        
        # Bar chart
        fig2.add_trace(
            go.Bar(x=[f"Class {i}" for i in range(len(probabilities))], 
                  y=probabilities,
                  marker_color='royalblue'),
            row=1, col=1
        )
        
        # Donut chart
        fig2.add_trace(
            go.Pie(labels=[f"Class {i}" for i in range(len(probabilities))],
                  values=probabilities,
                  hole=.4,
                  textinfo='label+percent'),
            row=1, col=2
        )
        
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Raw data
        with st.expander("📁 View Raw Prediction Data"):
            prob_df = pd.DataFrame({
                'Class': [f"Class {i}" for i in range(len(probabilities))],
                'Probability': probabilities,
                'Percentage': [f"{p*100:.2f}%" for p in probabilities]
            })
            st.dataframe(prob_df, use_container_width=True)
    
    # Model details section
    st.markdown("---")
    st.subheader("🔍 Model Details")
    
    tabs = st.tabs(["Model Info", "Training Data", "Export"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Model Parameters:**")
            st.code(f"""
            n_estimators: {model.n_estimators}
            max_depth: {model.max_depth if hasattr(model, 'max_depth') else 'Not set'}
            min_samples_split: {model.min_samples_split}
            random_state: {model.random_state if hasattr(model, 'random_state') else 'None'}
            """)
        
        with col2:
            st.markdown("**Model Stats:**")
            st.code(f"""
            Features: {model.n_features_in_}
            Classes: {model.n_classes_}
            Sample count: {model.n_samples_ if hasattr(model, '_n_samples') else 'Unknown'}
            """)
    
    with tabs[1]:
        if hasattr(model, 'estimators_'):
            st.info(f"Number of trees in forest: {len(model.estimators_)}")
            tree_depths = [tree.tree_.max_depth for tree in model.estimators_]
            avg_depth = np.mean(tree_depths)
            st.metric("Average Tree Depth", f"{avg_depth:.1f}")
        else:
            st.warning("Detailed tree data not available")
    
    with tabs[2]:
        st.download_button(
            label="📥 Download Predictions (CSV)",
            data=pd.DataFrame({'age': [age], 'budget': [budget]}).to_csv(index=False),
            file_name="prediction_input.csv",
            mime="text/csv"
        )
        
        st.download_button(
            label="📥 Download Model",
            data=open('ai_model.pkl', 'rb').read(),
            file_name="ai_model.pkl",
            mime="application/octet-stream"
        )

else:
    st.error("❌ MODEL FILE NOT FOUND")
    
    # Upload option
    uploaded_file = st.file_uploader("Upload your ai_model.pkl file", type=['pkl'])
    if uploaded_file:
        with open('ai_model.pkl', 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success("Model uploaded! Refresh the page.")

# Footer
st.markdown("---")
st.markdown("**Global Infrastructure AI Project** • Built with Streamlit")
