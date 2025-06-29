import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

st.set_page_config(page_title="SmartCast", layout="wide")

# تحميل النموذج
@st.cache_resource
def load_model():
    try:
        return joblib.load("xgb_model.joblib")
    except Exception as e:
        st.error(f"فشل في تحميل النموذج: {str(e)}")
        return None

model = load_model()

model_feature_order = [
    'Store', 'Dept', 'Holiday_Flag', 'Temperature', 'Fuel_Price',
    'CPI', 'Unemployment', 'Type', 'Size', 'Month',
    'Year', 'WeekOfYear', 'Quarter', 'Season', 'IsPromoWeek'
]

feature_info = {
    "Store": {"default": 22},
    "Dept": {"default": 50},
    "date": {"default": "2011-06-15"},
    "Holiday_Flag": {"default": 0},
    "Temperature": {"default": 70.0},
    "Fuel_Price": {"default": 3.25},
    "CPI": {"default": 185.0},
    "Unemployment": {"default": 7.5},
    "Type": {"default": "B"},
    "Size": {"default": 150000},
    "Month": {"default": 8},
    "Year": {"default": 2011},
    "WeekOfYear": {"default": 24},
    "Quarter": {"default": 2},
    "Season": {"default": 2},
    "IsPromoWeek": {"default": 0}
}

category_mapping = {"Type": {"A": 0, "B": 1, "C": 2}}

# العنوان
st.title("SmartCast - Sales Prediction")

# إدخال البيانات
st.subheader("أدخل البيانات للتنبؤ بالمبيعات:")
input_data = {}
cols = st.columns(2)

for i, feature in enumerate(model_feature_order):
    if feature == "Type":
        selected = cols[i % 2].selectbox(
            f"{feature}", ["A", "B", "C"], index=1
        )
        input_data[feature] = category_mapping["Type"][selected]

    elif feature == "date":
        date_val = pd.to_datetime(feature_info['date']['default']).date()
        input_data[feature] = cols[i % 2].date_input("تاريخ", value=date_val)

    elif feature in ["Holiday_Flag", "IsPromoWeek"]:
        input_data[feature] = int(cols[i % 2].selectbox(f"{feature}", ["0", "1"]))

    else:
        default_val = feature_info[feature]['default']
        input_data[feature] = cols[i % 2].number_input(f"{feature}", value=default_val)

# زر التنبؤ
if st.button("تنبؤ المبيعات"):
    if model:
        pred_df = pd.DataFrame([input_data])

        if "date" in pred_df.columns:
            pred_df["date"] = pd.to_datetime(pred_df["date"])
            pred_df["Year"] = pred_df["date"].dt.year
            pred_df["Month"] = pred_df["date"].dt.month
            pred_df["WeekOfYear"] = pred_df["date"].dt.isocalendar().week
            pred_df["Quarter"] = pred_df["date"].dt.quarter
            pred_df["Season"] = ((pred_df["Month"] % 12 + 3) // 3).map({
                1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 3,
                7: 3, 8: 3, 9: 4, 10: 4, 11: 4, 12: 1
            })
            pred_df.drop("date", axis=1, inplace=True)

        missing = [f for f in model_feature_order if f not in pred_df.columns]
        if missing:
            st.error(f"المدخلات ناقصة: {', '.join(missing)}")
        else:
            pred_df = pred_df[model_feature_order]
            try:
                prediction = model.predict(pred_df)[0]
                st.success(f"المبيعات المتوقعة: ${prediction:,.2f}")
            except Exception as e:
                st.error(f"فشل التنبؤ: {str(e)}")
    else:
        st.error("النموذج غير محمّل.")
