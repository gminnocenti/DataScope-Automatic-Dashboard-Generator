import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from dataframe_functions import fill_missing_values_numeric_columns,fill_missing_values_categorical_columns,advanced_analytics
st.title("Data Science Dashboard Generator")
st.write("Upload a CSV or Excel file to generate an interactive dashboard!")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])



def generate_dashboard(df):
    st.write("### Interactive Dashboard")
    num_cols = df.select_dtypes(include=np.number).columns
    if len(num_cols) > 0:
        st.write("#### Numeric Data Visualizations")
        selected_num_col = st.selectbox("Select a numeric column", num_cols)
        fig_hist = px.histogram(df, x=selected_num_col, title=f"Histogram of {selected_num_col}")
        st.plotly_chart(fig_hist)
    
    cat_cols = df.select_dtypes(exclude=np.number).columns
    if len(cat_cols) > 0:
        st.write("#### Categorical Data Visualizations")
        selected_cat_col = st.selectbox("Select a categorical column", cat_cols)
        fig_bar = px.bar(df[selected_cat_col].value_counts(), title=f"Bar Chart of {selected_cat_col}")
        st.plotly_chart(fig_bar)

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.write("### Uploaded Data Preview")
    st.dataframe(df.head())
    
    # Show statistics of numerical columns     
    st.write("### Summary Statistics")
    st.write(df.describe())
    df = fill_missing_values_numeric_columns(df)
    
    #Show statistics categorical columns
    cat_cols = df.select_dtypes(exclude=np.number).columns
    if len(cat_cols) > 0:
        st.write("#### Categorical Column Insights")
        for col in cat_cols:
            st.write(f"Value counts for {col}:")
            st.write(df[col].value_counts())
    
    df = fill_missing_values_categorical_columns(df)
    
    advanced_analytics(df)
    

    generate_dashboard(df)