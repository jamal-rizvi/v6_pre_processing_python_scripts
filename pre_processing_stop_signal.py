import numpy as np
import pandas as pd
import os

# Read the Excel file into a variable
gorilla_data = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(gorilla_data, 'stop_signal_v6.xlsx'))

# Extract the relevant columns from the DataFrame
# Include columns titled "Participant Private ID", "Task Name", "Display", "Screen", "Trial Number", "Response", "block", "Store: participant_display", "Store: worse", "Store: better",
df = df[["Participant Private ID", "Task Name", "Display", "Screen Counter", "Trial Number", "Response", "Correct", "Spreadsheet: Answer", 
         "Store: delay", "Store: reaction_time"]]

# Only include rows of the matrix that contain "go" or "stop" in the "Display" column
df = df[df['Display'].str.contains('go|stop', case=False, na=False)]

# Only include rows of the matrix that contain "3" in the "Screen Counter" column for the "go" trials
# Only include rows of the matrix that contain "4" in the "Screen Counter" column for the "stop" trials
df = df[((df['Display'].str.contains('go', case=False, na=False)) & (df['Screen Counter'] == 3)) | 
        ((df['Display'].str.contains('stop', case=False, na=False)) & (df['Screen Counter'] == 4))]

# Create variables for the different delay times (i.e. 50ms, 150ms, 250ms, 350ms)
# Each value in the "Store: delay" column (1, 2, 3, 4) will be mapped to the corresponding delay time (50ms, 150ms, 250ms, 350ms)
# These delay times will be stored in a new column called "delay_time"
# If the row is a "go" trial (in the Display column), the value in the "delay_time" column will be set to 0
delay_mapping = {1: 50, 2: 150, 3: 250, 4: 350}
df['delay_time'] = df['Store: delay'].map(delay_mapping)
df.loc[df['Display'].str.contains('go', case=False, na=False), 'delay_time'] = 0

# Append new column for correct response times for "go" trials 
df['go_correct_rt'] = np.where((df['Display'].str.contains('go', case=False, na=False)) & (df['Correct'] == 1), df['Store: reaction_time'], np.nan)

# Append new column for count of incorrect "stop" trials
df['stop_incorrect_count'] = np.where((df['Display'].str.contains('stop', case=False, na=False)) & (df['Correct'] == 0), 1, 0)

# Save the updated DataFrame to a new Excel file
df.to_excel('stop_signal_pre_processed_part1.xlsx', index=False)

# Read the Excel file into a new variable
filtered_data = os.path.dirname(os.path.abspath(__file__))
df2 = pd.read_excel(os.path.join(filtered_data, 'stop_signal_pre_processed_part1.xlsx'))

# Group the data by "Participant Private ID" and calculate the summary results for each participant
# Average reaction time for correct "go" trials will be the mean of the "go_correct_rt" column for each participant
# Total count of incorrect "stop" trials will be the sum of the "stop_incorrect_count" column for each participant
# Stop signal delay (SSD) will be the mean of the "delay_time" column for the "stop" trials for each participant
summary_df = df2.groupby('Participant Private ID').agg({
    'go_correct_rt': 'mean',    
    'stop_incorrect_count': 'sum',
    'delay_time': lambda x: x[df2['Display'].str.contains('stop', case=False, na=False)].mean()
}).reset_index()

# Calculate the sum of the delay times for the "stop" trials for each participant
summary_df['SSD_sum'] = df2[df2['Display'].str.contains('stop', case=False, na=False)].groupby('Participant Private ID')['delay_time'].sum().values

# Return the max number of "stop" trials for any participant (should be 50) in the Trial Number column
summary_df['stop_trials_total'] = df2[df2['Display'].str.contains('stop', case=False, na=False)].groupby('Participant Private ID')['Trial Number'].max().values

# Calculate the proportion of incorrect "stop" trials for each participant
summary_df['stop_incorrect_prob'] = summary_df['stop_incorrect_count'] / summary_df['stop_trials_total']

# Calculate stop signal reaction time (SSRT) for each participant using the integration method
# SSRT = mean go reaction time - mean stop signal delay
summary_df['SSRT'] = summary_df['go_correct_rt'] - (summary_df['SSD_sum'] / summary_df['stop_trials_total'])

print(summary_df)

# Save the summary DataFrame to a new Excel file
summary_df.to_excel('stop_signal_summary.xlsx', index=False)

# Read the summary Excel file into a variable
ssrt = os.path.dirname(os.path.abspath(__file__))
ssrt_df = pd.read_excel(os.path.join(ssrt, 'stop_signal_summary.xlsx'))

# Remove all columns except for "Participant Private ID" and "SSRT"
ssrt_df = ssrt_df[['Participant Private ID', 'SSRT']]
print(ssrt_df)

# Save the updated DataFrame to a new Excel file
ssrt_df.to_excel('stop_signal_SSRT.xlsx', index=False)