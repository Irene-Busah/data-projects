import pandas as pd
import streamlit as st

phone_data = pd.read_csv("phones_data.csv", index_col=0)

# cleaning the dataset
phone_data.fillna({"lowest_price": phone_data["lowest_price"].mean()}, inplace=True)

phone_data.fillna({"highest_price": phone_data["highest_price"].mean()}, inplace=True)
phone_data.dropna(
    subset=["os", "memory_size", "battery_size", "screen_size"], inplace=True
)

# streamlit app setup
st.title("Mobile Phone Price Comparison & Brand Performance Dashboard")

# sidebar filter
st.sidebar.header("Filters")
brand = st.sidebar.selectbox("Select Brand", phone_data["brand_name"].unique())
model = st.sidebar.selectbox(
    "Select Model", phone_data[phone_data["brand_name"] == brand]["model_name"].unique()
)


# filter day for select brand and model name
filtered_data = phone_data[
    (phone_data["brand_name"] == brand) & (phone_data["model_name"] == model)
]

# display the price information
st.subheader(f"Prices for {brand} {model}")
st.write(filtered_data[["best_price", "lowest_price", "highest_price"]])

# Explanation for price comparison
st.markdown(
    """
The table above shows the pricing information for the selected brand and model. 
- **Best Price**: This is the average best price at which the model is available.
- **Lowest Price**: This is the minimum price at which the model has been listed.
- **Highest Price**: This is the maximum price at which the model has been listed.
"""
)

# plot price comparison
st.subheader("Price Comparison")
st.bar_chart(filtered_data[["best_price", "lowest_price", "highest_price"]].transpose())


# brand performance
brand_summary = (
    phone_data.groupby("brand_name")
    .agg(
        {
            "popularity": "mean",
            "best_price": "mean",
            "lowest_price": "mean",
            "highest_price": "mean",
            "sellers_amount": "mean",
        }
    )
    .reset_index()
)

# Display brand performance summary
st.subheader("Brand Performance Report")
st.write(brand_summary)

# Explanation for brand performance
st.markdown(
    """
The table above summarizes the performance of each brand based on various metrics:
- **Popularity**: Average popularity score of the brand's models.
- **Best Price**: Average best price of the brand's models.
- **Lowest Price**: Average lowest price of the brand's models.
- **Highest Price**: Average highest price of the brand's models.
- **Market Presence**: Total number of sellers offering the brand's models.
"""
)

# Plot brand performance
st.subheader("Average Prices by Brand")
st.bar_chart(
    brand_summary.set_index("brand_name")[
        ["best_price", "lowest_price", "highest_price"]
    ]
)

# Explanation for average prices by brand
st.markdown(
    """
The bar chart above shows the average best, lowest, and highest prices for each brand. 
This allows users to compare the price range across different brands.
"""
)


st.subheader("Popularity by Brand")
st.bar_chart(brand_summary.set_index("brand_name")["popularity"])

# Explanation for popularity by brand
st.markdown(
    """
The bar chart above shows the average popularity score for each brand. 
This helps users understand which brands are more popular in the market.
"""
)

st.subheader("Market Presence by Brand (Number of Sellers)")
st.bar_chart(brand_summary.set_index("brand_name")["sellers_amount"])

# Explanation for market presence by brand
st.markdown(
    """
The bar chart above shows the total number of sellers offering models from each brand. 
This indicates the market presence and availability of the brand's models.
"""
)
