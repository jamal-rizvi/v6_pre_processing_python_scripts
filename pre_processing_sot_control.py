import numpy as np
import pandas as pd
import os

# Read the Excel file into a variable
gorilla_data = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(gorilla_data, 'sot_control_v6.xlsx'))

# Extract the relevant columns from the DataFrame
# Include columns titled "Participant Private ID", "Task Name", "Display", "Screen", "Trial Number", "Response", "block", "Store: participant_display", "Store: rank"
df = df[["Participant Private ID", "Task Name", "Display", "Screen", "Trial Number", "Response", "Spreadsheet: block", "Store: participant_display", "Store: rank"]]

# Remove all the rows of the matrix that don't contain "Screen 1" in the "Screen" column
df = df[df['Screen'] == 'Screen 1']

# Remove the rows of the matrix that don't contain "task" in the "Display" column
df = df[df['Display'].str.contains('task', case=False, na=False)]

# Save the updated DataFrame to a new Excel file
df.to_excel('sot_control_pre_processed_part1.xlsx', index=False)

# Read the Excel file into a new variable
filtered_data = os.path.dirname(os.path.abspath(__file__))
df2 = pd.read_excel(os.path.join(filtered_data, 'sot_control_pre_processed_part1.xlsx'))

# Change the name of the column titled "Store: participant_display" to "money_won"
df2 = df2.rename(columns={'Store: participant_display': 'money_won'})

# Append columns titled "better" and "worse" to the DataFrame, 
# "better" will be the count of all the occurences of "1" or "2" in the "Store: rank" column, 
# and "worse" will be the count of all the occurences of "3" or "4" in the "Store: rank" column
df2['better'] = df2['Store: rank'].apply(lambda x: sum([1 for i in str(x).split() if i in ['1', '2']]))
df2['worse'] = df2['Store: rank'].apply(lambda x: sum([1 for i in str(x).split() if i in ['3', '4']]))

# Append columns titled "Store: better" and "Store: worse" to the DataFrame,
# "Store: better" will be the cumulative sum of the "better" column per participant, and "Store: worse" will be the cumulative sum of the "worse" column per participant
# Each participant's data is grouped by the column "Participant Private ID", so the cumulative sum will reset for each participant
df2['Store: better'] = df2.groupby('Participant Private ID')['better'].cumsum()
df2['Store: worse'] = df2.groupby('Participant Private ID')['worse'].cumsum()

# "net_score" will be the value of "Store: worse" subtracted from "Store: better" (i.e. net_score = better - worse)
df2['net_score'] = df2['Store: better'] - df2['Store: worse']

# Save the updated DataFrame to a new Excel file
df2.to_excel('sot_control_pre_processed_part2.xlsx', index=False)

# Read the Excel file into a variable
summery_data = os.path.dirname(os.path.abspath(__file__))
df3 = pd.read_excel(os.path.join(summery_data, 'sot_control_pre_processed_part2.xlsx'))

# Group the data by "Participant ID" and calculate the summary results for each participant
# Total money won will be the value of the "money_won" column on the row where "Trial Number" is 50
# Net score will be the value of the "net_score" column on the row where "Trial Number" is 50
summary_df = df3[df3['Trial Number'] == 50].groupby('Participant Private ID').agg({'money_won': 'first', 'net_score': 'first'}).reset_index()
print(summary_df)

# Save the summary DataFrame to a new Excel file
summary_df.to_excel('sot_control_summary.xlsx', index=False)