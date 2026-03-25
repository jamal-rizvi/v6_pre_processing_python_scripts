import numpy as np
import pandas as pd
import os

# Read the Excel file into a variable
gorilla_data = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(gorilla_data, 'delay_discounting_v6.xlsx'))

# Extract the relevant columns from the DataFrame
# Include columns titled "Participant Private ID", "Task Name", "Display", "Trial Number", "Response", "block", "Store: participant_display", "Store: worse", "Store: better",
df = df[["Participant Private ID", "Task Name", "Display", "Spreadsheet: time_interval", "Store: count", "Store: now_value"]]

# Exclude rows of the matrix that contain "instructions" or "finish" in the "Display" column
df = df[~df['Display'].str.contains('instructions|finish', case=False, na=False)]

# Only include rows of the matrix that contain "1" in "Store: count" column
df = df[df['Store: count'] == 1]

# Save the updated DataFrame to a new Excel file
df.to_excel('delay_discounting_pre_processed_part1.xlsx', index=False)

# Read the Excel file into a new variable
filtered_data = os.path.dirname(os.path.abspath(__file__))
df2 = pd.read_excel(os.path.join(filtered_data, 'delay_discounting_pre_processed_part1.xlsx'))

# Creating new variables for storing data per participant
# If Display contains "1_week" then add value in the "Store: now_value" column to a new column called "value_1_week", 
# If Display contains "2_week" then add value in the "Store: now_value" column to a new column called "value_2_week",
# If Display contains "2_month" then add value in the "Store: now_value" column to a new column called "value_2_month",
# If Display contains "6_month" then add value in the "Store: now_value" column to a new column called "value_6_month",
# If Display contains "1_year" then add value in the "Store: now_value" column to a new column called "value_1_year",
# If Display contains "5_year" and does not contain "25_year" then add value in the "Store: now_value" column to a new column called "value_5_year", 
# If Display contains "25_year" then add value in the "Store: now_value" column to a new column called "value_25_year", 
df2['1 week'] = np.where(df2['Display'].str.contains('1_week', case=False, na=False), df2['Store: now_value'], np.nan)
df2['2 weeks'] = np.where(df2['Display'].str.contains('2_week', case=False, na=False), df2['Store: now_value'], np.nan)
df2['2 months'] = np.where(df2['Display'].str.contains('2_month', case=False, na=False), df2['Store: now_value'], np.nan)
df2['6 months'] = np.where(df2['Display'].str.contains('6_month', case=False, na=False), df2['Store: now_value'], np.nan)
df2['1 year'] = np.where(df2['Display'].str.contains('1_year', case=False, na=False), df2['Store: now_value'], np.nan)
df2['5 years'] = np.where(df2['Display'].str.contains('5_year', case=False, na=False) & ~df2['Display'].str.contains('25_year', case=False, na=False), df2['Store: now_value'], np.nan)
df2['25 years'] = np.where(df2['Display'].str.contains('25_year', case=False, na=False), df2['Store: now_value'], np.nan)

# Save the updated DataFrame to a new Excel file
df2.to_excel('delay_discounting_pre_processed_part2.xlsx', index=False)

# Read the Excel file into a variable
summary_data = os.path.dirname(os.path.abspath(__file__))
df3 = pd.read_excel(os.path.join(summary_data, 'delay_discounting_pre_processed_part2.xlsx'))

# Group the data by "Participant Private ID" and calculate the summary results for each participant
# Average value for each time interval will be the mean of the corresponding "value" column for each participant
summary_df = df3.groupby('Participant Private ID').agg({
    '1 week': 'mean',
    '2 weeks': 'mean',
    '2 months': 'mean',
    '6 months': 'mean',
    '1 year': 'mean',
    '5 years': 'mean',
    '25 years': 'mean'
}).reset_index().fillna(1000)

# Save the summary DataFrame to a new Excel file
summary_df.to_excel('delay_discounting_summary.xlsx', index=False)

# Read the summary Excel file into a variable
rates_data = os.path.dirname(os.path.abspath(__file__))
rates_df = pd.read_excel(os.path.join(rates_data, 'delay_discounting_summary.xlsx'))

# Calculate the discounting rate (k) for each time interval for each participant using the formula: k = ((1000 / value) - 1 )/ time_interval
time_intervals = {
    '1 week': 7,
    '2 weeks': 14,
    '2 months': 60,
    '6 months': 180,
    '1 year': 365,
    '5 years': 1825,
    '25 years': 9125
}
for interval, days in time_intervals.items():
    rates_df[f'k_{interval}'] = ((1000 / rates_df[interval]) - 1) / days

print(rates_df)

# Save the updated DataFrame with discounting rates to a new Excel file
rates_df.to_excel('delay_discounting_rates.xlsx', index=False)


# Reading task data into a dataframe
discounts = pd.read_excel(os.path.join(gorilla_data, 'delay_discounting_rates.xlsx'))

# select only columns that start with "k_"
discounts = discounts.filter(regex='^k_')

# Compute row-wise median of values > 0 and finite
k_med = discounts.apply(
    lambda row: np.median(row[(row > 0) & np.isfinite(row)]),
    axis=1
)

# Append the column with Participant Private ID to the k_med series
k_med = pd.concat([rates_df['Participant Private ID'], k_med.rename('k_median')], axis=1)

# Move the Participant Private ID column to the left of the k_median column
cols = k_med.columns.tolist()
cols.insert(cols.index('k_median'), cols.pop(cols.index('Participant Private ID')))

# Edit the "k_median" column title to "discount_rate"
k_med.rename(columns={'k_median': 'discount_rate'}, inplace=True)

print(k_med)

# Save the k_med DataFrame to a new Excel file
k_med.to_excel('delay_discounting_k_median.xlsx', index=False)