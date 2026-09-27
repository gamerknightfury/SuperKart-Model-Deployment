
import streamlit as st
import requests
import os

# Configure Streamlit page
st.set_page_config(
    page_title="SuperKart Sales Prediction",
    layout="centered"
)

# Backend API URL
# Inside the Docker network, the frontend communicates with the backend
# using the backend container/service name.
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://superkart-backend:7860/v1/predict"
)

# Page title and description
st.title("🛒 SuperKart Sales Prediction")
st.write(
    "Enter the product and store information below to predict "
    "the expected sales revenue."
)

st.divider()

# Input fields in two columns
col1, col2 = st.columns(2)

with col1:
    Product_Weight = st.number_input(
        "Product Weight",
        min_value=0.0,
        value=12.66
    )

    Product_Sugar_Content = st.selectbox(
        "Product Sugar Content",
        ["Low Sugar", "Regular", "No Sugar"]
    )

    Product_Allocated_Area = st.number_input(
        "Product Allocated Area",
        min_value=0.0,
        value=0.068
    )

    Product_MRP = st.number_input(
        "Product MRP",
        min_value=0.0,
        value=147.0
    )

    Store_Size = st.selectbox(
        "Store Size",
        ["Small", "Medium", "High"]
    )

with col2:
    Store_Location_City_Type = st.selectbox(
        "Store Location City Type",
        ["Tier 1", "Tier 2", "Tier 3"]
    )

    Store_Type = st.selectbox(
        "Store Type",
        [
            "Supermarket Type1",
            "Supermarket Type2",
            "Departmental Store",
            "Food Mart"
        ]
    )

    Store_Age_Years = st.number_input(
        "Store Age (Years)",
        min_value=0,
        value=17
    )

    Product_Type_Category = st.selectbox(
        "Product Type Category",
        ["Perishables", "Non-Perishables"]
    )

    Product_Id_char = st.selectbox(
        "Product ID Category",
        ["FD", "NC", "DR"]
    )

st.divider()

# Run prediction
if st.button("Predict Sales", type="primary", use_container_width=True):

    if Product_Weight == 0:
        st.warning("Please enter a valid Product Weight.")

    elif Product_MRP == 0:
        st.warning("Please enter a valid Product MRP.")

    else:
        # Prepare input data for Flask API
        product_data = {
            "Product_Weight": Product_Weight,
            "Product_Sugar_Content": Product_Sugar_Content,
            "Product_Allocated_Area": Product_Allocated_Area,
            "Product_MRP": Product_MRP,
            "Store_Size": Store_Size,
            "Store_Location_City_Type": Store_Location_City_Type,
            "Store_Type": Store_Type,
            "Store_Age_Years": Store_Age_Years,
            "Product_Type_Category": Product_Type_Category,
            "Product_Id_char": Product_Id_char
        }

        try:
            with st.spinner("Generating prediction..."):

                response = requests.post(
                    BACKEND_URL,
                    json=product_data,
                    timeout=30
                )

            if response.status_code == 200:
                result = response.json()
                predicted_sales = result["predicted_sales"]

                st.success("Prediction completed successfully!")

                st.metric(
                    label="Predicted Sales",
                    value=f"{predicted_sales:,.2f}"
                )

            else:
                st.error(
                    f"Prediction request failed: {response.text}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Unable to connect to the prediction API: {e}")
