import pandas as pd
import matplotlib.pyplot as plt
import math

# Load the data
file_path = 'housing_market_data.csv'
data = pd.read_csv(file_path)

# Convert 'DATE' to datetime format
data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')

# Handle missing values by filling them forward
data.fillna(method='ffill', inplace=True)

# Display the first few rows
print(data.head())

# Determine the number of rows and columns for the grid
num_columns = 4
num_plots = len(data.columns) - 1  # Excluding the 'DATE' column
num_rows = math.ceil(num_plots / num_columns)

fig, axs = plt.subplots(num_rows, num_columns, figsize=(20, num_rows * 5))
axs = axs.flatten()

# Plotting each column
for i, column in enumerate(data.columns[1:]):  # Excluding the 'DATE' column
    axs[i].plot(data['DATE'], data[column])
    axs[i].set_title(column)
    axs[i].set_xlabel('Date')
    axs[i].set_ylabel(column)

# Remove any empty subplots
for j in range(i + 1, len(axs)):
    fig.delaxes(axs[j])

# Adjust layout
plt.tight_layout(pad=5.0)  # Adding spacing between plots
plt.show()
