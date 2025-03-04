import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Data Science Dashboard Generator")
st.write("Upload a CSV or Excel file to generate an interactive dashboard!")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

# Updated clean_data function from above
def clean_data(df):
    st.write("### Data Cleaning Options")
    
    # Remove duplicates (immediate action, no button needed here)
    if st.checkbox("Remove duplicates"):
        df = df.drop_duplicates()
        st.write("Duplicates removed!")

    # Handle missing values
    st.write("#### Handle Missing Values")
    missing_option = st.selectbox(
        "Choose a method", 
        ["Drop rows with missing values", "Fill with mean (numeric)", "Fill with mode (categorical)", "Leave as is", "Apply same method to all columns"]
    )

    # Get columns with missing values
    cols_with_missing = df.columns[df.isnull().any()].tolist()
    
    # Variable to track if cleaning was applied
    cleaning_applied = False

    if cols_with_missing:
        # Define UI elements based on selected method
        if missing_option == "Drop rows with missing values":
            selected_cols = st.multiselect(
                "Select columns to drop rows with missing values (or leave empty to apply to all)", 
                cols_with_missing
            )
            if st.button("Apply Cleaning"):
                if selected_cols:
                    df = df.dropna(subset=selected_cols)
                else:
                    df = df.dropna()
                st.write("Rows with missing values dropped!")
                cleaning_applied = True

        elif missing_option == "Fill with mean (numeric)":
            numeric_cols = df.select_dtypes(include=np.number).columns
            numeric_cols_with_missing = [col for col in numeric_cols if col in cols_with_missing]
            if numeric_cols_with_missing:
                selected_cols = st.multiselect(
                    "Select numeric columns to fill with mean (or leave empty to apply to all numeric)", 
                    numeric_cols_with_missing
                )
                if st.button("Apply Cleaning"):
                    if selected_cols:
                        df[selected_cols] = df[selected_cols].fillna(df[selected_cols].mean())
                    else:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled with mean!")
                    cleaning_applied = True
            else:
                st.write("No numeric columns with missing values found.")

        elif missing_option == "Fill with mode (categorical)":
            cat_cols = df.select_dtypes(exclude=np.number).columns
            cat_cols_with_missing = [col for col in cat_cols if col in cols_with_missing]
            if cat_cols_with_missing:
                selected_cols = st.multiselect(
                    "Select categorical columns to fill with mode (or leave empty to apply to all categorical)", 
                    cat_cols_with_missing
                )
                if st.button("Apply Cleaning"):
                    if selected_cols:
                        df[selected_cols] = df[selected_cols].fillna(df[selected_cols].mode().iloc[0])
                    else:
                        df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])
                    st.write("Missing values filled with mode!")
                    cleaning_applied = True
            else:
                st.write("No categorical columns with missing values found.")

        elif missing_option == "Apply same method to all columns":
            all_cols_method = st.selectbox(
                "Choose a method for all columns",
                ["Drop rows with missing values", "Fill with mean (numeric only)", "Fill with mode (all columns)"]
            )
            if st.button("Apply Cleaning"):
                if all_cols_method == "Drop rows with missing values":
                    df = df.dropna()
                    st.write("Rows with missing values dropped from all columns!")
                elif all_cols_method == "Fill with mean (numeric only)":
                    numeric_cols = df.select_dtypes(include=np.number).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values in numeric columns filled with mean!")
                elif all_cols_method == "Fill with mode (all columns)":
                    df = df.fillna(df.mode().iloc[0])
                    st.write("Missing values in all columns filled with mode!")
                cleaning_applied = True

        elif missing_option == "Leave as is":
            st.write("No changes will be made to missing values unless you select another option.")

        # Show preview only if cleaning was applied
        if cleaning_applied:
            st.write("### Cleaned Data Preview")
            st.dataframe(df.head())
    else:
        st.write("No missing values found in the dataset.")

    # Always return the DataFrame, cleaned or not
    return df
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
    
    df_cleaned = clean_data(df)
    st.write("### Summary Statistics")
    st.write(df_cleaned.describe())
    
    cat_cols = df_cleaned.select_dtypes(exclude=np.number).columns
    if len(cat_cols) > 0:
        st.write("#### Categorical Column Insights")
        for col in cat_cols:
            st.write(f"Value counts for {col}:")
            st.write(df_cleaned[col].value_counts())
    
    generate_dashboard(df_cleaned)