COVID-19 Forecasting System
Overview
This project provides a system to track COVID-19 cases in South Africa and predict the number of new cases over the next seven days using ARIMA modeling. The system involves scraping the latest COVID-19 statistics, applying machine learning to forecast future cases, and presenting the results via a web interface.

Components
1. Data Ingestion
The system scrapes the number of daily COVID-19 cases in South Africa from Worldometers.

URL: https://www.worldometers.info/coronavirus/country/south-africa/
The scraping is performed using BeautifulSoup to extract the daily cases.
2. Modeling
The data is processed and modeled using the ARIMA (AutoRegressive Integrated Moving Average) method from the statsmodels library.

ARIMA is used to predict new COVID-19 cases for the next seven days based on past data.
The model is trained using daily new cases obtained from the scraped data.
3. Simple Reporting
The forecast results (for the next 7 days) are saved in a CSV file: forecasted_covid_data_7_days.csv.
A time series plot of the forecasted data is saved as a PNG file: forecast_plot.png.
A .txt file with recommendations for improving the forecasting system is generated.
4. Web Application (Bonus Task)
A simple web interface displays the forecasting results in a table and as time series plots.
The API provides two routes: /forecast and /original, exposing the forecasted and original COVID-19 data.
Project Structure
.
├── 2024 ASSESSMENT/
│   ├── app.py                    # Flask app for API
│   ├── forecast.js               # JavaScript for frontend (API interaction and plotting)
│   ├── forecasted_covid_data_7_days.json  # Forecasted data in JSON format
│   ├── index.html                # Frontend HTML page
│   ├── main.py                   # Main script that runs the entire system
│   ├── model.py                  # Data scraping, processing, and forecasting script
│   ├── original_covid_data.json   # Original COVID-19 data in JSON format
│   ├── style.css                 # CSS file for the frontend
├── README.md                     # Project documentation
Setup Instructions
Prerequisites
Python 3.8+

pip (Python package installer)

Install the required libraries by running:

pip install -r requirements.txt
Alternatively, the main.py script will check and install any missing packages automatically.

Running the Project
Step 1: Run the main.py script:

This will scrape data, process it, forecast the next 7 days, save the results, start the Flask server, and open the web interface.
python main.py
Step 2: Open the web interface:

The script will automatically open the default browser to display the forecast results.
Alternatively, manually visit: http://127.0.0.1:5000/ in your browser.
API Endpoints
/forecast: Returns the forecasted COVID-19 data for the next 7 days in JSON format.
/original: Returns the original COVID-19 case data.
Data Files
original_covid_data.json: Contains the original data with the historical COVID-19 cases.
forecasted_covid_data_7_days.json: Contains the forecasted data for the next 7 days.
Output Files
CSV: The forecasted new cases are saved as a CSV file (forecasted_covid_data_7_days.csv).
PNG: A time series plot of the forecasted new cases is saved as a PNG file (forecast_plot.png).
TXT: A paragraph recommending improvements for forecasting accuracy is saved in forecast_recommendations.txt.
Improving the System
To improve forecast accuracy, consider incorporating additional data like:

Vaccination Rates: More vaccinations reduce the spread and therefore lower new cases.
Lockdown/Policy Measures: Stringency of government restrictions can affect case trends.
Hospital Data: Information on hospital admissions and recoveries may give insights into future case trends.