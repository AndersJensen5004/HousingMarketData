import pandas as pd
from fredapi import Fred

# Import the API key from config.py
from config import API_KEY

# Initialize the Fred instance
fred = Fred(api_key=API_KEY)

# Function to fetch data from FRED
def fetch_data(series_id, start_date):
    try:
        data = fred.get_series(series_id, start_date)
        return pd.DataFrame(data, columns=[series_id])
    except ValueError as e:
        print(f"Error fetching data for series ID '{series_id}': {e}")
        return None

# List of relevant series IDs
series_ids = {
    'Housing Starts': 'HOUST',
    'Real Median Household Income': 'MEHOINUSA672N',
    'Rental Vacancy Rate': 'RRVRUSQ156N',
    'New One Family Houses Sold': 'HSN1F',
    '30-Year Fixed Mortgage Rate': 'MORTGAGE30US',
    'Unemployment Rate': 'UNRATE',
    'Consumer Price Index': 'CPIAUCSL',
    'Consumer Confidence Index': 'UMCSENT',
    'Building Permits': 'PERMIT',
    'Personal Income': 'PI',
    'Nonfarm Payrolls': 'PAYEMS',
    '10-Year Treasury Yield': 'DGS10',
    'S&P 500': 'SP500',
    'Delinquency Rate on All Loans': 'DRALACBS',
    'Median Home Price': 'MSPUS',
}

# Start date for data collection
start_date = '2000-01-01'

# Fetch and combine data
data_frames = []
for name, series_id in series_ids.items():
    df = fetch_data(series_id, start_date)
    if df is not None:
        df.columns = [name]
        data_frames.append(df)

combined_data = pd.concat(data_frames, axis=1)

# Reset index to get 'DATE' as a column and rename it
combined_data.reset_index(inplace=True)
combined_data.rename(columns={'index': 'DATE'}, inplace=True)

# Save to CSV
combined_data.to_csv('housing_market_data.csv', index=False)

print(combined_data.head())

