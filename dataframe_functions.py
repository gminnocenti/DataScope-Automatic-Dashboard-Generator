import streamlit as st
import pandas as pd
import numpy as np



def fill_missing_values_numeric_columns(df):
    st.write("#### Handle Missing Numeric Values")
    missing_option = st.selectbox(
        "Choose a method", 
        ["Drop rows with missing values", "Fill with mean", "Fill with median", "Fill with weighted average", "Interpolate", "Leave as is"]
    )

    cols_with_missing = df.columns[df.isnull().any()].tolist()
    numeric_cols = df.select_dtypes(include=np.number).columns
    cols_with_missing_numerical = [col for col in numeric_cols if col in cols_with_missing]

    cleaning_applied = False

    if cols_with_missing_numerical:
        if missing_option == "Drop rows with missing values":
            selected_cols = st.multiselect(
                "Select columns to drop rows with missing values (or leave empty to apply to all numeric)", 
                cols_with_missing_numerical
            )
            if st.button("Apply Numeric Cleaning"):
                if selected_cols:
                    df = df.dropna(subset=selected_cols)
                else:
                    df = df.dropna(subset=cols_with_missing_numerical)
                st.write("Rows with missing values dropped!")
                cleaning_applied = True

        elif missing_option == "Fill with mean":
            selected_cols = st.multiselect(
                "Select numeric columns to fill with mean (or leave empty to apply to all numeric with missing values)", 
                cols_with_missing_numerical
            )
            if st.button("Apply Numeric Cleaning"):
                if selected_cols:
                    df[selected_cols] = df[selected_cols].fillna(df[selected_cols].mean())
                else:
                    df[cols_with_missing_numerical] = df[cols_with_missing_numerical].fillna(df[cols_with_missing_numerical].mean())
                st.write("Missing values filled with mean!")
                cleaning_applied = True

        elif missing_option == "Fill with median":
            selected_cols = st.multiselect(
                "Select numeric columns to fill with median (or leave empty to apply to all numeric with missing values)", 
                cols_with_missing_numerical
            )
            if st.button("Apply Numeric Cleaning"):
                if selected_cols:
                    df[selected_cols] = df[selected_cols].fillna(df[selected_cols].median())
                else:
                    df[cols_with_missing_numerical] = df[cols_with_missing_numerical].fillna(df[cols_with_missing_numerical].median())
                st.write("Missing values filled with median!")
                cleaning_applied = True

        elif missing_option == "Fill with weighted average":
            selected_cols = st.multiselect(
                "Select numeric columns to fill with weighted average (or leave empty to apply to all numeric with missing values)", 
                cols_with_missing_numerical
            )
            weight_col = st.selectbox(
                "Select a column to use as weights", 
                numeric_cols
            )
            if st.button("Apply Numeric Cleaning"):
                if selected_cols:
                    for col in selected_cols:
                        weighted_avg = np.average(df[col].dropna(), weights=df[weight_col].dropna())
                        df[col] = df[col].fillna(weighted_avg)
                else:
                    for col in cols_with_missing_numerical:
                        weighted_avg = np.average(df[col].dropna(), weights=df[weight_col].dropna())
                        df[col] = df[col].fillna(weighted_avg)
                st.write("Missing values filled with weighted average!")
                cleaning_applied = True

        elif missing_option == "Interpolate":
            selected_cols = st.multiselect(
                "Select numeric columns to interpolate (or leave empty to apply to all numeric with missing values)", 
                cols_with_missing_numerical
            )
            if st.button("Apply Numeric Cleaning"):
                if selected_cols:
                    df[selected_cols] = df[selected_cols].interpolate(method='linear', limit_direction='both')
                else:
                    df[cols_with_missing_numerical] = df[cols_with_missing_numerical].interpolate(method='linear', limit_direction='both')
                st.write("Missing values filled with linear interpolation!")
                cleaning_applied = True

        elif missing_option == "Leave as is":
            st.write("No changes will be made to missing numeric values.")

        if cleaning_applied:
            st.write("### Cleaned Numeric Data Preview")
            st.dataframe(df.head())
    else:
        st.write("No numeric columns with missing values found in the dataset.")
    
    return df

def fill_missing_values_categorical_columns(df):
    st.write("#### Handle Missing Categorical Values")
    missing_option = st.selectbox(
        "Choose a method", 
        ["Drop rows with missing values", "Fill with mode (categorical)", "Leave as is"]
    )

    cols_with_missing = df.columns[df.isnull().any()].tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns
    cols_with_missing_categorical = [col for col in cat_cols if col in cols_with_missing]

    cleaning_applied = False

    if cols_with_missing_categorical:
        if missing_option == "Drop rows with missing values":
            selected_cols = st.multiselect(
                "Select columns to drop rows with missing values (or leave empty to apply to all categorical)", 
                cols_with_missing_categorical
            )
            if st.button("Apply Categorical Cleaning"):
                if selected_cols:
                    df = df.dropna(subset=selected_cols)
                else:
                    df = df.dropna(subset=cols_with_missing_categorical)
                st.write("Rows with missing values dropped!")
                cleaning_applied = True

        elif missing_option == "Fill with mode (categorical)":
            selected_cols = st.multiselect(
                "Select categorical columns to fill with mode (or leave empty to apply to all categorical)", 
                cols_with_missing_categorical
            )
            if st.button("Apply Categorical Cleaning"):
                if selected_cols:
                    df[selected_cols] = df[selected_cols].fillna(df[selected_cols].mode().iloc[0])
                else:
                    df[cols_with_missing_categorical] = df[cols_with_missing_categorical].fillna(df[cols_with_missing_categorical].mode().iloc[0])
                st.write("Missing values filled with mode!")
                cleaning_applied = True

        elif missing_option == "Leave as is":
            st.write("No changes will be made to missing categorical values.")

        if cleaning_applied:
            st.write("### Cleaned Categorical Data Preview")
            st.dataframe(df.head())
    else:
        st.write("No categorical columns with missing values found in the dataset.")
    
    return df

