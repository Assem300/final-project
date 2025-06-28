import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import base64

# Configuration
st.set_page_config(
    page_title="SmartCast",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# SmartCast - Advanced Forecasting System"
    }
)

# Custom CSS for vibrant design
st.markdown("""
<style>
    :root {
        --primary: #6C63FF;
        --secondary: #FF6584;
        --accent: #20C997;
        --dark: #2C3E50;
        --light: #F8F9FA;
        --warning: #FFC107;
    }
    
    body {
        background-color: #F5F7FF;
        color: var(--dark);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #F5F7FF 0%, #E6E9FF 100%);
    }
    
    .stApp {
        background: transparent;
    }
    
    .header {
        background: linear-gradient(90deg, var(--primary) 0%, #8A7CFF 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.2);
        margin-bottom: 2rem;
    }
    
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border: none;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .feature-title {
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .feature-badge {
        display: inline-block;
        background: rgba(108, 99, 255, 0.1);
        color: var(--primary);
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.75rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .btn-primary {
        background: linear-gradient(90deg, var(--primary) 0%, #8A7CFF 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(108, 99, 255, 0.25) !important;
        transition: all 0.3s !important;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(108, 99, 255, 0.35) !important;
    }
    
    .btn-secondary {
        background: linear-gradient(90deg, var(--secondary) 0%, #FF8A9D 100%) !important;
        border: none !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8F9FA 100%);
        box-shadow: 5px 0 15px rgba(0, 0, 0, 0.03);
    }
    
    .st-bb {
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .stNumberInput, .stSelectbox, .stTextInput {
        margin-bottom: 1rem;
    }
    
    .stNumberInput input, .stSelectbox select, .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }
    
    .prediction-result {
        background: linear-gradient(90deg, var(--accent) 0%, #38D9A9 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(32, 201, 151, 0.2);
        margin-top: 1.5rem;
    }
    
    .prediction-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .uploaded-data {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
    }
    
    .validation-success {
        color: var(--accent);
        font-weight: 600;
    }
    
    .validation-error {
        color: var(--secondary);
        font-weight: 600;
    }
    
    .tab-content {
        padding: 1rem 0;
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: #6C757D;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    try:
        return joblib.load("xgb_model.joblib")
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None

model = load_model()

# Define the correct feature order expected by the model
model_feature_order = [
    'Store', 'Dept', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 
    'CPI', 'Unemployment', 'Type', 'Size', 'Month', 
    'Year', 'WeekOfYear', 'Quarter', 'Season', 'IsPromoWeek'
]

# Updated feature information
feature_info = {
    "Store": {
        "description": "Unique identifier for each store",
        "range": "1 to 45 (integer)",
        "example": "1, 2, 3,...",
        "icon": "🏪",
        "default": 22
    },
    "Dept": {
        "description": "Department number within the store",
        "range": "1 to 99 (integer)",
        "example": "1, 2, 3,...",
        "icon": "📦",
        "default": 50
    },
    "date": {
        "description": "Week of the sale (YYYY-MM-DD format)",
        "range": "2010-02-05 to 2012-11-23",
        "example": "2010-02-05, 2012-11-23,...",
        "icon": "📅",
        "default": "2011-06-15"
    },
    "Weekly_Sales": {
        "description": "Cleaned weekly sales figures",
        "range": "Positive numbers",
        "example": "24924.5, 66836.92,...",
        "icon": "💰"
    },
    "Holiday_Flag": {
        "description": "Holiday indicator",
        "range": "0 or 1",
        "example": "0 = No, 1 = Yes",
        "icon": "🏷️",
        "default": 0
    },
    "Temperature": {
        "description": "Average temperature during the week",
        "range": "30 to 110 (Fahrenheit)",
        "example": "42.31, 78.50,...",
        "icon": "🌡️",
        "default": 70.0
    },
    "Fuel_Price": {
        "description": "Fuel price in the store's region",
        "range": "2.0 to 4.5 (dollars)",
        "example": "2.72, 3.14,...",
        "icon": "⛽",
        "default": 3.25
    },
    "CPI": {
        "description": "Consumer Price Index",
        "range": "120 to 250",
        "example": "126.06, 138.33,...",
        "icon": "📊",
        "default": 185.0
    },
    "Unemployment": {
        "description": "Unemployment rate",
        "range": "3.0 to 15.0 (percentage)",
        "example": "5.8, 7.2,...",
        "icon": "📉",
        "default": 7.5
    },
    "Type": {
        "description": "Store type (A, B, or C)",
        "range": "A, B, or C",
        "example": "A = Small, B = Medium, C = Large",
        "icon": "🏬",
        "default": "B"
    },
    "Size": {
        "description": "Size of the store in square feet",
        "range": "20,000 to 250,000",
        "example": "151315, 202307,...",
        "icon": "📏",
        "default": 150000
    },
    "Month": {
        "description": "Month of the year",
        "range": "1 to 12",
        "example": "1 (Jan), 6 (Jun), 12 (Dec)",
        "icon": "📅",
        "default": 8
    },
    "Year": {
        "description": "Year of the record",
        "range": "2010 to 2012",
        "example": "2010, 2011, 2012",
        "icon": "📅",
        "default": 2011
    },
    "WeekOfYear": {
        "description": "Week number of the year",
        "range": "1 to 52",
        "example": "5, 23, 50",
        "icon": "📅",
        "default": 24
    },
    "Quarter": {
        "description": "Quarter of the year",
        "range": "1 to 4",
        "example": "1 (Q1), 2 (Q2), 3 (Q3), 4 (Q4)",
        "icon": "📅",
        "default": 2
    },
    "Season": {
        "description": "Season of the year",
        "range": "1 to 4 (1=Winter, 2=Spring, 3=Summer, 4=Fall)",
        "example": "1, 2, 3, 4",
        "icon": "🌞",
        "default": 2
    },
    "IsPromoWeek": {
        "description": "Whether the week includes a promotion",
        "range": "0 or 1",
        "example": "0 = No, 1 = Yes",
        "icon": "🏷️",
        "default": 0
    }
}

category_mapping = {
    "Type": {"A": 0, "B": 1, "C": 2}
}

# App Header
st.markdown('<div class="header"><h1 style="color:white; margin:0;">✨ SmartCast </h1><p style="color:white; margin:0; opacity:0.8;">Advanced Retail Sales Forecasting System</p></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:2rem;">
        <h2 style="color:var(--primary); margin-bottom:0.5rem;">🔮 Insights Manual</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align:center; margin-bottom:1rem;">
        <h3 style="color:var(--primary); margin-bottom:0.5rem;">📚 Feature Guide</h3>
        <p style="font-size:0.9rem; color:#6C757D;">Click to expand each feature</p>
    </div>
    """, unsafe_allow_html=True)
    
    for feature, info in feature_info.items():
        with st.expander(f"{info['icon']} {feature}"):
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-title">{info['icon']} {feature}</div>
                <p style="margin-bottom:0.75rem;">{info['description']}</p>
                <span class="feature-badge">Range: {info['range']}</span>
                <span class="feature-badge">Example: {info['example']}</span>
            </div>
            """, unsafe_allow_html=True)

# Real-time Prediction
st.markdown("""
<div class="card">
    <h2 style="color:var(--primary); margin-top:0;">🔮 Real-time Sales Prediction</h2>
    <p style="color:#6C757D;">Fill in the details below to get an instant sales prediction</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    input_data = {}
    cols = st.columns(2)
    
    for i, feature in enumerate(model_feature_order):
        if feature in ["Weekly_Sales"]:
            continue  # Skip target variable
            
        info = feature_info.get(feature, {
            "icon": "🔹",
            "description": f"{feature} information",
            "range": "N/A",
            "example": "N/A",
            "default": 0
        })
        
        with cols[i % 2]:
            if feature == "Type":
                options = list(category_mapping["Type"].keys())
                selected = st.selectbox(
                    f"{info['icon']} {feature}",
                    options,
                    index=options.index(info.get('default', 'B')),
                    help=info['description']
                )
                input_data[feature] = category_mapping["Type"][selected]
            elif feature == "date":
                # Parse date range from feature info
                date_range = info['range'].split(" to ")
                min_date = pd.to_datetime(date_range[0]).date()
                max_date = pd.to_datetime(date_range[1]).date()
                default_date = pd.to_datetime(info['default']).date()
                
                input_data[feature] = st.date_input(
                    f"{info['icon']} {feature}",
                    value=default_date,
                    min_value=min_date,
                    max_value=max_date,
                    help=info['description']
                )
            elif feature in ["Holiday_Flag", "IsPromoWeek"]:
                option = st.selectbox(
                    f"{info['icon']} {feature}",
                    ["0", "1"],
                    index=info.get('default', 0),
                    help=info['description']
                )
                input_data[feature] = int(option)
            else:
                # Parse numeric ranges from feature info
                range_parts = info['range'].split("(")[0].strip().split(" to ")
                if len(range_parts) == 2:
                    try:
                        min_val = float(range_parts[0]) if "." in range_parts[0] else int(range_parts[0])
                        max_val = float(range_parts[1]) if "." in range_parts[1] else int(range_parts[1])
                        default_val = info.get('default', 0)
                        
                        input_data[feature] = st.number_input(
                            f"{info['icon']} {feature}",
                            min_value=min_val,
                            max_value=max_val,
                            value=default_val,
                            step=1.0 if isinstance(default_val, int) else 0.01,
                            help=info['description']
                        )
                    except:
                        input_data[feature] = st.number_input(
                            f"{info['icon']} {feature}",
                            value=info.get('default', 0),
                            help=info['description']
                        )
                else:
                    input_data[feature] = st.number_input(
                        f"{info['icon']} {feature}",
                        value=info.get('default', 0),
                        help=info['description']
                    )

    if st.button("✨ Predict Sales", key="predict_single", use_container_width=True):
        if model:
            # Prepare the input data for prediction
            pred_df = pd.DataFrame([input_data])
            
            # Convert date to features if needed
            if "date" in pred_df.columns:
                pred_df["date"] = pd.to_datetime(pred_df["date"])
                pred_df["Year"] = pred_df["date"].dt.year
                pred_df["Month"] = pred_df["date"].dt.month
                pred_df["WeekOfYear"] = pred_df["date"].dt.isocalendar().week
                pred_df["Quarter"] = pred_df["date"].dt.quarter
                # Simple season calculation (1=Winter, 2=Spring, 3=Summer, 4=Fall)
                pred_df["Season"] = ((pred_df["Month"] % 12 + 3) // 3).map({1:1, 2:1, 3:2, 4:2, 5:2, 6:3, 7:3, 8:3, 9:4, 10:4, 11:4, 12:1})
                pred_df = pred_df.drop("date", axis=1)
            
            # Ensure all required features are present
            missing_features = [f for f in model_feature_order if f not in pred_df.columns]
            
            if missing_features:
                st.error(f"Missing required features: {', '.join(missing_features)}")
            else:
                try:
                    # Reorder columns to match model expectations
                    pred_df = pred_df[model_feature_order]
                    
                    # Make prediction
                    prediction = model.predict(pred_df)[0]

                    if prediction < 1:
                        formatted_prediction = f"${int(prediction * 1000)}K"
                    else:
                        formatted_prediction = f"${prediction:,.2f}M"
                    
                    with col2:
                        st.markdown(f"""
                        <div class="prediction-result">
                            <h3 style="margin-top:0;">Predicted Sales</h3>
                            <div class="prediction-value">{formatted_prediction}</div>
                            <p style="margin-bottom:0;">for the given parameters</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class="card" style="margin-top:1.5rem;">
                            <h3 style="color:var(--primary); margin-top:0;">📊 Insights</h3>
                            <p>This prediction is based on:</p>
                            <ul>
                                <li>Advanced machine learning model</li>
                                <li>Historical sales patterns</li>
                                <li>Current market conditions</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")
        else:
            st.error("Model not loaded. Cannot make predictions.")

# Footer
st.markdown("""
<div class="footer">
    <p>✨ SmartCast | Powered by XGBoost | © 2025 Retail Analytics</p>
    <p style="font-size:0.8rem; opacity:0.7;">For support contact: support@SmartCast.ai</p>
</div>
""", unsafe_allow_html=True)
