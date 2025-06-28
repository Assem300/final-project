import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# تنسيق الأرقام الكبيرة
def format_number(number):
    if number >= 1_000_000_000:
        return "${:.2f}B".format(number / 1_000_000_000)
    elif number >= 1_000_000:
        return "${:.2f}M".format(number / 1_000_000)
    else:
        return "${:,.2f}".format(number)

def render_overview(selected_year, df):
    filtered_df = df[df['Year'] == selected_year]

    # KPIs
    total_sales_value = filtered_df['Weekly_Sales'].sum()
    average_sales_value = filtered_df['Weekly_Sales'].mean()
    top_store_id = filtered_df.groupby('Store')['Weekly_Sales'].sum().idxmax()

    total_sales = format_number(total_sales_value)
    average_sales = format_number(average_sales_value)
    top_store_text = f"Store {top_store_id}"

    # البيانات للرسم
    weekly_sales = filtered_df.groupby('Date')['Weekly_Sales'].sum().reset_index()
    department_sales = filtered_df.groupby('Dept')['Weekly_Sales'].sum().reset_index()
    promo_sales = filtered_df[filtered_df['IsPromoWeek'] == 1].groupby('Date')['Weekly_Sales'].sum().reset_index()
    non_promo_sales = filtered_df[filtered_df['IsPromoWeek'] == 0].groupby('Date')['Weekly_Sales'].sum().reset_index()

    # عنوان القسم
    st.subheader("Overview of Sales Performance")

    # KPIs Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", total_sales)
    with col2:
        st.metric("Average Weekly Sales", average_sales)
    with col3:
        st.metric("Top Store", top_store_text)

    # Weekly Sales Over Time
    fig1 = px.line(weekly_sales, x='Date', y='Weekly_Sales', title='Weekly Sales Over Time')
    st.plotly_chart(fig1, use_container_width=True)

    # Sales by Department
    col4, col5 = st.columns(2)
    with col4:
        fig2 = px.bar(department_sales, x='Dept', y='Weekly_Sales', title='Sales by Department',
                      labels={'Dept': 'Department', 'Weekly_Sales': 'Sales'})
        st.plotly_chart(fig2, use_container_width=True)

    # Promo vs Non-Promo
    with col5:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=promo_sales['Date'], y=promo_sales['Weekly_Sales'], name='Promo Sales'))
        fig3.add_trace(go.Bar(x=non_promo_sales['Date'], y=non_promo_sales['Weekly_Sales'], name='Non-Promo Sales'))
        fig3.update_layout(title='Promo vs Non-Promo Performance', xaxis_title='Date', yaxis_title='Sales', barmode='group')
        st.plotly_chart(fig3, use_container_width=True)
