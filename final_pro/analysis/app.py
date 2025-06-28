import streamlit as st
import pandas as pd
from overview import render_overview  # تأكد أن هذه الدوال متوافقة مع Streamlit
from sales_trends import render_sales_trends
from department_performance import render_department_performance
from seasonality_analysis import render_seasonality_analysis

# تحميل البيانات
df = pd.read_csv('walmart_cleaned.csv')

# تجهيز عمود التاريخ
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
else:
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + df['WeekOfYear'].astype(str) + '0', format='%Y%W%w')

# السنوات المتاحة
years_available = sorted(df['Year'].unique())

# تصميم الواجهة
st.set_page_config(layout="wide", page_title="Walmart Sales Dashboard")

# شعار


# عنوان
st.title("Walmart Sales Dashboard")

# اختيار التبويب
tab = st.selectbox("اختر القسم:", [
    'Overview',
    'Sales Trends',
    'Performance by Department',
    'Seasonality Analysis'
])

# اختيار السنة
selected_year = st.selectbox("اختر السنة:", years_available)

# عرض المحتوى بناءً على التبويب
if tab == 'Overview':
    render_overview(selected_year, df)
elif tab == 'Sales Trends':
    render_sales_trends(selected_year, df)
elif tab == 'Performance by Department':
    render_department_performance(selected_year, df)
elif tab == 'Seasonality Analysis':
    render_seasonality_analysis(selected_year, df)
