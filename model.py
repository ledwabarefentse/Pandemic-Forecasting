# Install libraries

import subprocess
import sys
import importlib

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = [
    'requests', 'beautifulsoup4', 'pandas', 'numpy', 'statsmodels', 
    'scikit-learn', 'matplotlib', 'seaborn', 'flask', 'selenium', 
    'webdriver-manager', 'scrapy', 'scrapy-splash', 'docker', 'ace_tools'
]

# Check and install packages if not present
for package in required_packages:
    try:
        importlib.import_module(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found. Installing...")
        install_package(package)

print("All required packages are installed.")

# Import Libraries

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import json
import os
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from datetime import datetime

# Scrape Data

# URL of the page you want to scrape
url = 'https://www.worldometers.info/coronavirus/country/south-africa/'

# Send an HTTP request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the <script> tags in the HTML
    scripts = soup.find_all('script')

    # Loop through the scripts to find the one with the Highcharts data
    for script in scripts:
        if 'Highcharts.chart' in script.text and 'coronavirus-cases-linear' in script.text:
            highcharts_script = script.text
            break
    else:
        highcharts_script = None

    # If the Highcharts script was found, extract the data
    if highcharts_script:
        print("Found Highcharts script. Extracting data...")

        # Use regex to extract the categories (dates) and series (data points)
        categories_pattern = re.search(r'categories: \[(.*?)\]', highcharts_script)
        data_pattern = re.search(r'data: \[(.*?)\]', highcharts_script)

        if categories_pattern and data_pattern:
            # Extract the dates and data points
            categories_str = categories_pattern.group(1)
            data_str = data_pattern.group(1)

            # Clean and split the data
            categories = json.loads(f"[{categories_str}]")
            data = json.loads(f"[{data_str}]")

            # Convert string dates to datetime objects
            dates = [datetime.strptime(date.strip('"'), '%b %d, %Y') for date in categories]

        else:
            print("Could not extract data or categories from the script.")
    else:
        print("No Highcharts chart configuration found in the page's scripts.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Model

# Create a DataFrame with dates and cumulative total cases
df = pd.DataFrame({'Date': dates, 'Cases': data})
df.set_index('Date', inplace=True)

# Calculate daily new cases from the cumulative total cases
df['New Cases'] = df['Cases'].diff().dropna()

# Fit ARIMA model on the daily new cases
model = ARIMA(df['New Cases'].dropna(), order=(5, 1, 2))  # adjust (p,d,q) for better performance
model_fit = model.fit()

# Forecast the next 7 days of new cases
forecast = model_fit.forecast(steps=7)
forecast_dates = pd.date_range(df.index[-1], periods=8, freq='D')[1:]

# Convert forecast into a DataFrame for plotting and rounding
forecast_df = pd.DataFrame({
    'Date': forecast_dates, 
    'New Cases': forecast,
})

# Add a rounded-off column for better readability
forecast_df['Rounded Cases'] = forecast_df['New Cases'].round()

# Set 'Date' as the index
forecast_df.set_index('Date', inplace=True)

# Calculate cumulative sum of forecasted new cases
forecast_df['Cumulative Cases'] = forecast_df['New Cases'].cumsum() + df['Cases'][-1]

# Save Data

# Function to save DataFrame as JSON
def save_to_json(dataframe, file_name):
    file_path = os.path.join(os.getcwd(), file_name)

    # Convert the index (Date) to strings to make it JSON serializable
    dataframe.index = dataframe.index.astype(str)

    dataframe.to_json(file_path, orient='table', indent=4)
    print(f"Data saved as JSON at: {file_path}")

# Original data saving (Assume 'dates' and 'data' are already populated from earlier)
df = pd.DataFrame({'Date': dates, 'Cases': data})
df.set_index('Date', inplace=True)

# Save original data as JSON
save_to_json(df, "original_covid_data.json")

# Function to save forecasted data (7 days forecast)
def save_forecast_to_json(forecast_df, file_name):
    file_path = os.path.join(os.getcwd(), file_name)

    # Limit forecast to just 7 days
    forecast_df = forecast_df.head(7)

    # Convert the index (Date) to strings to make it JSON serializable
    forecast_df.index = forecast_df.index.astype(str)

    # Save forecasted data to JSON
    with open(file_path, 'w') as f:
        json.dump(forecast_df.to_dict(orient='index'), f, indent=4)

    print(f"Forecasted data (7 days) saved as JSON at: {file_path}")

# Save forecasted data (7 days)
save_forecast_to_json(forecast_df, "forecasted_covid_data_7_days.json")