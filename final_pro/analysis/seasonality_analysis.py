import streamlit as st
import plotly.express as px
import pandas as pd

def render_seasonality_analysis(selected_year, df):
    # تصفية البيانات حسب السنة المختارة
    filtered_df = df[df['Year'] == selected_year]

    # إجمالي المبيعات حسب المواسم
    sales_by_season = (
        filtered_df.groupby('Season')['Weekly_Sales']
        .sum()
        .reset_index()
    )

    # رسم مبيعات المواسم
    seasonality_fig = px.bar(
        sales_by_season,
        x='Season',
        y='Weekly_Sales',
        title='Sales by Season',
        labels={'Weekly_Sales': 'Sales'}
    )
    seasonality_fig.update_layout(title_x=0.5)

    # مقارنة المبيعات في أسابيع العروض مقابل غيرها
    promo_sales = (
        filtered_df.groupby('IsPromoWeek')['Weekly_Sales']
        .mean()
        .reset_index()
    )
    promo_sales['Promo'] = promo_sales['IsPromoWeek'].map({False: 'Non-Promo', True: 'Promo'})

    promo_fig = px.bar(
        promo_sales,
        x='Promo',
        y='Weekly_Sales',
        title='Promo vs Non-Promo Sales',
        labels={'Weekly_Sales': 'Average Sales'}
    )
    promo_fig.update_layout(title_x=0.5)

    # عرض الرسوم في Streamlit
    st.plotly_chart(seasonality_fig, use_container_width=True)
    st.plotly_chart(promo_fig, use_container_width=True)
