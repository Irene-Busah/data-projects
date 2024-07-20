# Mobile Phone Price Comparison and Brand Performance Dashboard

This project provides an interactive dashboard to compare mobile phone prices and analyze brand performance based on various metrics. It leverages data on mobile phones' pricing, popularity, and specifications to deliver insights into market trends and brand competitiveness.

## Project Description

This project combines two key functionalities:
1. **Price Comparison Dashboard**: Allows users to select a specific brand and model to view detailed pricing information, including best price, lowest price, and highest price.
2. **Brand Performance Report**: Provides summary statistics for each brand, including average prices, popularity scores, and the number of sellers offering the brand's models.

The data is visualized using interactive charts to make the analysis more accessible and insightful for users.

## Dataset Description

The dataset contains information on various mobile phone models, including:
- **Brand Name**: The manufacturer of the mobile phone.
- **Model Name**: The specific model of the mobile phone.
- **OS**: The operating system of the mobile phone.
- **Popularity**: An index representing the popularity of the mobile phone.
- **Best Price**: The best average price at which the mobile phone is available.
- **Lowest Price**: The minimum price at which the mobile phone has been listed.
- **Highest Price**: The maximum price at which the mobile phone has been listed.
- **Sellers Amount**: The number of sellers offering the mobile phone.
- **Screen Size**: The size of the mobile phone screen in inches.
- **Memory Size**: The size of the mobile phone memory in GB.
- **Battery Size**: The size of the mobile phone battery in mAh.
- **Release Date**: The release date of the mobile phone.

## Usage

To use this project, you need to run the Streamlit app. The app provides an interactive interface where you can filter the data and view the analysis.

### Instructions

1. Install the required packages:
   ```bash
   pip install pandas streamlit
2. Run the Streamlit app:
    ```bash
    streamlit run app.py
3. Use the sidebar filters to select a brand and model, and explore the price comparison and brand performance reports.

### Features
1. Interactive Filters: Easily filter data by brand and model to view specific price comparisons.
2. Visualized Data: Bar charts to compare prices and analyze brand performance.
3. Summary Statistics: Aggregated data to provide insights into brand popularity and market presence.