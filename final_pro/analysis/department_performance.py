import streamlit as st
import plotly.express as px

def render_department_performance(selected_year, df):
    filtered_df = df[df['Year'] == selected_year]

    # حساب مبيعات كل قسم
    department_sales = (
        filtered_df.groupby('Dept')['Weekly_Sales']
        .sum()
        .reset_index()
        .sort_values(by='Weekly_Sales', ascending=False)
    )

    # رسم بياني باستخدام Plotly Express
    fig = px.bar(
        department_sales,
        x='Dept',
        y='Weekly_Sales',
        title='Department Performance',
        labels={'Dept': 'Department', 'Weekly_Sales': 'Total Sales'}
    )

    # عرض الرسم البياني في Streamlit
    st.plotly_chart(fig, use_container_width=True)
