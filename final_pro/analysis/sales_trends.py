import streamlit as st
import plotly.express as px
import pandas as pd

def render_sales_trends(selected_year, df):
    filtered_df = df[df['Year'] == selected_year]

    # تجهيز البيانات
    weekly_sales = filtered_df.groupby('Date')['Weekly_Sales'].sum().reset_index()
    monthly_sales = filtered_df.groupby('Month')['Weekly_Sales'].sum().reset_index()
    holiday_sales = filtered_df.groupby('Holiday_Flag')['Weekly_Sales'].mean().reset_index()
    holiday_sales['Holiday_Type'] = holiday_sales['Holiday_Flag'].map({0: 'Non-Holiday', 1: 'Holiday'})

    # رسم Weekly Sales
    fig_weekly = px.line(
        weekly_sales,
        x='Date',
        y='Weekly_Sales',
        title='Weekly Sales Over Time',
        labels={'Weekly_Sales': 'Sales'},
    )
    fig_weekly.update_layout(hovermode='x unified')
    st.plotly_chart(fig_weekly, use_container_width=True)

    # تقسيم لصفين: شهري وأيام العطلات
    col1, col2 = st.columns(2)

    with col1:
        fig_monthly = px.bar(
            monthly_sales,
            x='Month',
            y='Weekly_Sales',
            title='Sales by Month',
            labels={'Month': 'Month', 'Weekly_Sales': 'Sales'}
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    with col2:
        fig_holiday = px.bar(
            holiday_sales,
            x='Holiday_Type',
            y='Weekly_Sales',
            title='Average Sales: Holiday vs Non-Holiday',
            labels={'Holiday_Type': 'Holiday', 'Weekly_Sales': 'Avg Weekly Sales'}
        )
        st.plotly_chart(fig_holiday, use_container_width=True)
