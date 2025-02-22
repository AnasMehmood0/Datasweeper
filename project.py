# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the title of the app
st.set_page_config(page_title="Data Shredder", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
st.title("Data Sweeper – Simplify Your Data Cleaning | By Anas Mehmood")
st.write("Easily refine your data with our cleaning tool! Simply upload your file and utilize our features to optimize and perfect your information.")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: rgb(87, 87, 238);
        color: rgb(252, 252, 252);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Upload file
uploaded_files = st.file_uploader("Upload a file (accepts CSV & Excel): ", type=["csv", "xlsx"], accept_multiple_files=True)

# Check if files are uploaded
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file) 
        else:
            st.error(f"Please upload a CSV or Excel file: {file_ext} is not supported")
            continue

        # Display the DataFrame
        st.write("Get a glimpse of the DataFrame head:")
        st.write(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Choices")

        # Show column names
        if st.checkbox(f"Show column names: {file.name}"):
            st.write(df.columns.tolist())

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates removed.")

        with col2:
            if st.button("Fill missing values with column mean"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Empty fields have been populated.")

        # Select columns to keep
        st.subheader("Select Columns to Keep")
        selected_columns = st.multiselect(f"Select columns to keep for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show data visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:  # Excel
                df.to_excel(buffer, index=False, engine="xlsxwriter")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"Click to download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )

            st.success("File has been converted successfully!")
