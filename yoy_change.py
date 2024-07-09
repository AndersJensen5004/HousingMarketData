import pandas as pd
import numpy as np

# Load the data
file_path = 'housing_market_data.csv'
data = pd.read_csv(file_path)

# Convert 'DATE' to datetime format
data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')

# Set 'DATE' as the index
data.set_index('DATE', inplace=True)

# Create an empty DataFrame to store YoY changes
yoy_data = pd.DataFrame(index=data.index)

# Define a mapping of columns to their frequency
column_frequencies = {
    'Housing Starts': 'M',
    'Real Median Household Income': 'A',
    'Existing Home Sales': 'M',
    'Rental Vacancy Rate': 'Q',
    'New One Family Houses Sold': 'M',
    '30-Year Fixed Mortgage Rate': 'M',
    'Unemployment Rate': 'M',
    'Consumer Price Index': 'M',
    'Consumer Confidence Index': 'M',
    'Building Permits': 'M',
    'Personal Income': 'M',
    'Nonfarm Payrolls': 'M',
    '10-Year Treasury Yield': 'M',
    'S&P 500': 'M',
    'Delinquency Rate on All Loans': 'Q',
    'Median Home Price': 'Q',
}

# Calculate YoY change for each column
for column, freq in column_frequencies.items():
    if column in data.columns:
        try:
            if freq == 'M':
                # For monthly data, resample to end of month and calculate YoY change
                monthly_data = data[column].resample('ME').last()
                yoy_change = monthly_data.pct_change(periods=12, fill_method=None)
            elif freq == 'Q':
                # For quarterly data, resample to end of quarter and calculate YoY change
                quarterly_data = data[column].resample('QE').last()
                yoy_change = quarterly_data.pct_change(periods=4, fill_method=None)
                # Forward fill the quarterly changes to monthly frequency
                yoy_change = yoy_change.resample('ME').ffill()
            elif freq == 'A':
                # For annual data, resample to end of year and calculate YoY change
                annual_data = data[column].resample('YE').last()
                yoy_change = annual_data.pct_change(periods=1, fill_method=None)
                # Forward fill the annual changes to monthly frequency
                yoy_change = yoy_change.resample('ME').ffill()
            else:
                yoy_change = data[column].pct_change(periods=12, fill_method=None)  # Default to monthly

            yoy_data[column] = yoy_change
        except Exception as e:
            print(f"Error processing column {column}: {e}")
    else:
        print(f"Column '{column}' not found in the data.")

# Resample yoy_data to monthly frequency, using the last day of each month
yoy_data = yoy_data.resample('ME').last()

# Handle NaN values by forward filling within each column
yoy_data = yoy_data.fillna(method='ffill')

# Save to a new CSV
yoy_data.to_csv('housing_market_yoy_change.csv')

# Display the first few rows of the YoY data
print(yoy_data.head())