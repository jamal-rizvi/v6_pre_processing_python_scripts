import numpy as np
import pandas as pd
import os

# Read the Excel file into a variable
gorilla_data = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(gorilla_data, 'win_lose_v6.xlsx'))

# Extracting the relevant columns for pre-processing
# Exclude columns titled Event Index	UTC Timestamp	UTC Date and Time	Local Timestamp	Local Timezone	Local Date and Time	Experiment ID	Experiment Version	Tree Node Key	Repeat Key	Schedule ID	Participant Public ID
# Exclude columns titled Participant Starting Group	Participant Status	Participant Completion Code	Participant External Session ID	Participant Device Type	Participant Device	Participant OS	Participant Browser	Participant Monitor Size	Participant Viewport Size	Checkpoint	Room ID	Room Order	Task Name	Task Version	Manipulation: Spreadsheet	Current Spreadsheet
# Exclude columns titled Screen ID	Screen Counter	Response Type   Context 	Onset Time	Clock Time	Reaction Time	Absolute Onset Time	Absolute Clock Time	Absolute Reaction Time	Correct	Response Duration	Proportion
# Exclude columns titled Component Name	Object Name	Object Number	Object ID
df = df.drop(columns=['Event Index', 'UTC Timestamp', 'UTC Date and Time', 'Local Timestamp', 'Local Timezone', 'Local Date and Time', 'Experiment ID', 'Experiment Version', 'Tree Node Key', 'Repeat Key', 'Schedule ID', 'Participant Public ID',
                       'Participant Starting Group', 'Participant Status', 'Participant Completion Code', 'Participant External Session ID', 'Participant Device Type', 'Participant Device', 'Participant OS', 'Participant Browser', 'Participant Monitor Size', 'Participant Viewport Size', 'Checkpoint', 'Room ID', 'Room Order', 'Task Version', 'Manipulation: Spreadsheet', 'Current Spreadsheet',
                       'Screen ID', 'Screen Counter', 'Response Type', 'Context', 'Onset Time', 'Clock Time', 'Reaction Time', 'Absolute Onset Time', 'Absolute Clock Time', 'Absolute Reaction Time', 'Correct', 'Response Duration', 'Proportion',
                       'Component Name', 'Object Name', 'Object Number', 'Object ID'])

# Simplifying column names by removing the prefix "Spreadsheet: " from all of the column headings where it appears
df.columns = df.columns.str.replace('Spreadsheet: ', '')

# Replace the prefix "Store: " in column names with "DV: " to indicate that these columns contain dependent variable data
df.columns = df.columns.str.replace('Store: ', 'DV: ')

# Remove all the rows of the matrix that don't contain "Screen 1" in the "Screen" column
df = df[df['Screen'] == 'Screen 1']

# Remove the rows of the matrix that don't contain "task" in the "Display" column
df = df[df['Display'].str.contains('task', case=False, na=False)]

# Append columns to the right of the existing columns of the data frame
# The new columns will be titled "DV: myopic choice", "DV: prospective choice", "DV: myopic wins", "DV: prospective wins"
# "DV: myopic choice" will sum the values from "DV: myopic_choice_3" and "DV: myopic_choice_4"
# "DV: prospective choice" will sum the values from "DV: prospective_choice_1" and "DV: prospective_choice_2"
# "DV: myopic wins" will sum the values from "DV: myopic_wins_3" and "DV: myopic_wins_4"
# "DV: prospective wins" will sum the values from "DV: prospective_wins_1" and "DV: prospective_wins_2"
df['DV: myopic_choice'] = df['DV: myopic_choice_3'] + df['DV: myopic_choice_4']
df['DV: prospective_choice'] = df['DV: prospective_choice_1'] + df['DV: prospective_choice_2']
df['DV: myopic_wins'] = df['DV: myopic_wins_3'] + df['DV: myopic_wins_4']
df['DV: prospective_wins'] = df['DV: prospective_wins_1'] + df['DV: prospective_wins_2']

# Append columns to the right of the existing columns of the data frame
# The new columns will be titled "DV: myopic actions", "DV: prospective actions"
# "DV: myopic actions" will sum the values from "DV: myopic_choice" and "DV: myopic_wins"
# "DV: prospective actions" will sum the values from "DV: prospective_choice" and "DV: prospective_wins"
df['DV: myopic_actions'] = df['DV: myopic_choice'] + df['DV: myopic_wins']
df['DV: prospective_actions'] = df['DV: prospective_choice'] + df['DV: prospective_wins']

# Append columns to the right of the existing columns of the data frame
# The new columns will be titled "DV: myopic_persistence", "DV: myopic_reinforcement", "DV: prospective_persistence", "DV: prospective_reinforcement",
# "DV: myopic_persistence" will return 1 if "DV: myopic_actions" is 1 and "DV: myopic_choice" from the previous row is 1, otherwise it will return 0
# "DV: myopic_reinforcement" will return 1 if "DV: myopic_actions" is 1 and "DV: myopic_wins" from the previous row is 1, otherwise it will return 0
# "DV: prospective_persistence" will return 1 if "DV: prospective_actions" is 1 and "DV: prospective_choice" from the previous row is 1, otherwise it will return 0
# "DV: prospective_reinforcement" will return 1 if "DV: prospective_actions" is 1 and "DV: prospective_wins" from the previous row is 1, otherwise it will return 0
df['DV: myopic_persistence'] = ((df['DV: myopic_actions'] == 1) & (df['DV: myopic_choice'].shift(1) == 1)).astype(int)
df['DV: myopic_reinforcement'] = ((df['DV: myopic_actions'] == 1) & (df['DV: myopic_wins'].shift(1) == 1)).astype(int)
df['DV: prospective_persistence'] = ((df['DV: prospective_actions'] == 1) & (df['DV: prospective_choice'].shift(1) == 1)).astype(int)
df['DV: prospective_reinforcement'] = ((df['DV: prospective_actions'] == 1) & (df['DV: prospective_wins'].shift(1) == 1)).astype(int)

# Append columns to the right of the existing columns of the data frame
# The new columns will be titled "DV: myopic_curiosity", "DV: myopic_switch", "DV: prospective_curiosity", "DV: prospective_switch"
# "DV: myopic_curiosity" will return 1 if "DV: myopic_actions" is 1 and "DV: prospective_choice" from the previous row is 1, otherwise it will return 0
# "DV: myopic_switch" will return 1 if "DV: myopic_actions" is 1 and "DV: prospective_wins" from the previous row is 1, otherwise it will return 0
# "DV: prospective_curiosity" will return 1 if "DV: prospective_actions" is 1 and "DV: myopic_choice" from the previous row is 1, otherwise it will return 0
# "DV: prospective_switch" will return 1 if "DV: prospective_actions" is 1 and "DV: myopic_wins" from the previous row is 1, otherwise it will return 0
df['DV: myopic_curiosity'] = ((df['DV: myopic_actions'] == 1) & (df['DV: prospective_choice'].shift(1) == 1)).astype(int)
df['DV: myopic_switch'] = ((df['DV: myopic_actions'] == 1) & (df['DV: prospective_wins'].shift(1) == 1)).astype(int)
df['DV: prospective_curiosity'] = ((df['DV: prospective_actions'] == 1) & (df['DV: myopic_choice'].shift(1) == 1)).astype(int)
df['DV: prospective_switch'] = ((df['DV: prospective_actions'] == 1) & (df['DV: myopic_wins'].shift(1) == 1)).astype(int)

# Append columns to the right of the existing columns of the data frame
# The new columns will be titled "DV: myopic_exploit", "DV: myopic_explore", "DV: prospective_exploit", "DV: prospective_explore", "DV: total_exploit", "DV: total_explore"
# "DV: myopic_exploit" will return 1 if "DV: myopic_persistence" is 1 or "DV: myopic_reinforcement" is 1, otherwise it will return 0
# "DV: myopic_explore" will return 1 if "DV: myopic_curiosity" is 1 or "DV: myopic_switch" is 1, otherwise it will return 0
# "DV: prospective_exploit" will return 1 if "DV: prospective_persistence" is 1 or "DV: prospective_reinforcement" is 1, otherwise it will return 0
# "DV: prospective_explore" will return 1 if "DV: prospective_curiosity" is 1 or "DV: prospective_switch" is 1, otherwise it will return 0
# "DV: total_exploit" will return 1 if "DV: myopic_exploit" is 1 or "DV: prospective_exploit" is 1, otherwise it will return 0
# "DV: total_explore" will return 1 if "DV: myopic_explore" is 1 or "DV: prospective_explore" is 1, otherwise it will return 0
df['DV: myopic_exploit'] = ((df['DV: myopic_persistence'] == 1) | (df['DV: myopic_reinforcement'] == 1)).astype(int)
df['DV: myopic_explore'] = ((df['DV: myopic_curiosity'] == 1) | (df['DV: myopic_switch'] == 1)).astype(int)
df['DV: prospective_exploit'] = ((df['DV: prospective_persistence'] == 1) | (df['DV: prospective_reinforcement'] == 1)).astype(int)
df['DV: prospective_explore'] = ((df['DV: prospective_curiosity'] == 1) | (df['DV: prospective_switch'] == 1)).astype(int)
df['DV: total_exploit'] = ((df['DV: myopic_exploit'] == 1) | (df['DV: prospective_exploit'] == 1)).astype(int)
df['DV: total_explore'] = ((df['DV: myopic_explore'] == 1) | (df['DV: prospective_explore'] == 1)).astype(int)

# Append columns to the right of the existing columns of the data frame 
# The new columns will be titled "DV: myopic_model-free", "DV: myopic_model-based", "DV: prospective_model-free", "DV: prospective_model-based", "DV: total_model-free", "DV: total_model-based"
# "DV: myopic_model-free" will return 1 if "DV: myopic_reinforcement" is 1 or "DV: myopic_curiosity" is 1, otherwise it will return 0
# "DV: myopic_model-based" will return 1 if "DV: myopic_persistence" is 1 or "DV: myopic_switch" is 1, otherwise it will return 0
# "DV: prospective_model-free" will return 1 if "DV: prospective_reinforcement" is 1 or "DV: prospective_curiosity" is 1, otherwise it will return 0
# "DV: prospective_model-based" will return 1 if "DV: prospective_persistence" is 1 or "DV: prospective_switch" is 1, otherwise it will return 0
# "DV: total_model-free" will return 1 if "DV: myopic_model-free" is 1 or "DV: prospective_model-free" is 1, otherwise it will return 0
# "DV: total_model-based" will return 1 if "DV: myopic_model-based" is 1 or "DV: prospective_model-based" is 1, otherwise it will return 0
df['DV: myopic_model-free'] = ((df['DV: myopic_reinforcement'] == 1) | (df['DV: myopic_curiosity'] == 1)).astype(int)
df['DV: myopic_model-based'] = ((df['DV: myopic_persistence'] == 1) | (df['DV: myopic_switch'] == 1)).astype(int)
df['DV: prospective_model-free'] = ((df['DV: prospective_reinforcement'] == 1) | (df['DV: prospective_curiosity'] == 1)).astype(int)
df['DV: prospective_model-based'] = ((df['DV: prospective_persistence'] == 1) | (df['DV: prospective_switch'] == 1)).astype(int)
df['DV: total_model-free'] = ((df['DV: myopic_model-free'] == 1) | (df['DV: prospective_model-free'] == 1)).astype(int)
df['DV: total_model-based'] = ((df['DV: myopic_model-based']    == 1) | (df['DV: prospective_model-based'] == 1)).astype(int)
print(df)


# Save the updated DataFrame to a new Excel file
df.to_excel('win_lose_pre_processed_part1.xlsx', index=False)

# Read the Excel file into a variable
filtered_data = os.path.dirname(os.path.abspath(__file__))
df2 = pd.read_excel(os.path.join(filtered_data, 'win_lose_pre_processed_part1.xlsx'))

# Filtering irrelevant columns for data-analysis
# Exclude columns titled Screen display	A_PRE	A_POST	B_PRE	B_POST	C_PRE	C_POST	D_PRE	D_POST	A_RESULT	B_RESULT	C_RESULT	D_RESULT
# Exclude columns titled pre_1	penalty_1	result_1	pre_2	penalty_2	result_2	pre_3	penalty_3	result_3	pre_4	penalty_4	result_4	myopic_choice_2	myopic_choice_3	both_mc	prospective_choice_1	prospective_choice_4	both_pc	myopic_wins_2	myopic_wins_3	both_mw	prospective_wins_1	both_pw	both_pw_mc	prospective_wins_4	prospective_persistence_1	prospective_persistence_4	myopic_persistence_2	myopic_persistence_3	prospective_reinforcement_1	prospective_reinforcement_4	myopic_reinforcement_2	myopic_reinforcement_3	prospective_curiosity_1	prospective_curiosity_4	myopic_curiosity_2	myopic_curiosity_3	prospective_switch_1	prospective_switch_4	myopic_switch_2	myopic_switch_3	both_pp	both_mp	both_pr	both_mr	both_pcu	both_mcu	both_ma	both_pa	both_psw	both_msw	myopic_action_2	myopic_action_3	prospective_action_1	prospective_action_4	myopic_exploit	myopic_explore	prospective_exploit	prospective_explore	total_explore	total_exploit	myopic_model_free	myopic_model_based	prospective_model_free	prospective_model_based	total_model_free	total_model_based
df2 = df2.drop(columns=['Screen', 'Display', 'display', 'Tag', 'A_PRE', 'A_POST', 'B_PRE', 'B_POST', 'C_PRE', 'C_POST', 'D_PRE', 'D_POST', 'A_RESULT', 'B_RESULT', 'C_RESULT', 'D_RESULT',
                       'pre_1', 'penalty_1', 'result_1', 'pre_2', 'penalty_2', 'result_2', 'pre_3', 'penalty_3', 'result_3', 'pre_4', 'penalty_4', 'result_4', 'myopic_choice_3', 'myopic_choice_4', 
                       'both_mc', 'prospective_choice_1', 'prospective_choice_2', 'both_pc', 'myopic_wins_4', 'myopic_wins_3', 'both_mw', 'prospective_wins_1', 'both_pw', 'both_pw_mc', 
                       'prospective_wins_2', 'prospective_persistence_1', 'prospective_persistence_2', 'myopic_persistence_4', 'myopic_persistence_3', 'prospective_reinforcement_1', 
                       'prospective_reinforcement_2', 'myopic_reinforcement_4', 'myopic_reinforcement_3', 'prospective_curiosity_1', 'prospective_curiosity_2', 'myopic_curiosity_4', 
                       'myopic_curiosity_3', 'prospective_switch_1', 'prospective_switch_2', 'myopic_switch_4', 'myopic_switch_3', 'both_pp', 'both_mp', 'both_pr', 'both_mr', 'both_pcu', 
                       'both_mcu', 'both_ma', 'both_pa', 'both_psw', 'both_msw', 'myopic_action_4', 'myopic_action_3', 'prospective_action_1', 'prospective_action_2', 'myopic_exploit', 
                       'myopic_explore', 'prospective_exploit', 'prospective_explore', 'total_explore', 'total_exploit', 'myopic_model_free', 'myopic_model_based', 'prospective_model_free', 
                       'prospective_model_based', 'total_model_free', 'total_model_based', 'DV: progress'])

# Change the name of the column titled "DV: participant display" to "DV: money_won"
df2 = df2.rename(columns={'DV: participant_display': 'DV: money_won'})

# "DV: net_score" will be the value of "DV: worse" subtracted from "DV: better" (i.e. net_score = better - worse)
df2['DV: net_score'] = df2['DV: better'] - df2['DV: worse']

# Append "DV: net_score" column to the right of the column titled "DV: better"
better_index = df2.columns.get_loc('DV: better')
df2.insert(better_index + 1, 'DV: net_score', df2.pop('DV: net_score'))

# Simplifying column names by removing the prefix "DV: " from all of the column headings where it appears
df2.columns = df2.columns.str.replace('DV: ', '')
print(df2)

# Save the updated DataFrame to a new Excel file
df2.to_excel('win_lose_pre_processed_part2.xlsx', index=False)

# Read the Excel file into a variable
summery_data = os.path.dirname(os.path.abspath(__file__))
df3 = pd.read_excel(os.path.join(summery_data, 'win_lose_pre_processed_part2.xlsx'))

# Group the data by "Participant ID" and calculate the summary results for each participant
# Total money won will be the value of the "money_won" column on the row where "Trial Number" is 50
# Net score will be the value of the "net_score" column on the row where "Trial Number" is 50
# Myopic choices will be the sum of the "myopic_choice" column for each participant, Prospective choices will be the sum of the "prospective_choice" column for each participant
# Myopic wins will be the sum of the "myopic_wins" column for each participant, Prospective wins will be the sum of the "prospective_wins" column for each participant
# Myopic actions will be the sum of the "myopic_actions" column for each participant, Prospective actions will be the sum of the "prospective_actions" column for each participant
# Myopic persistence will be the sum of the "myopic_persistence" column for each participant, Prospective persistence will be the sum of the "prospective_persistence" column for each participant
# Myopic reinforcement will be the sum of the "myopic_reinforcement" column for each participant, Prospective reinforcement will be the sum of the "prospective_reinforcement" column for each participant
# Myopic curiosity will be the sum of the "myopic_curiosity" column for each participant, Prospective curiosity will be the sum of the "prospective_curiosity" column for each participant
# Myopic switch will be the sum of the "myopic_switch" column for each participant, Prospective switch will be the sum of the "prospective_switch" column for each participant
# Myopic explore will be the sum of the "myopic_explore" column for each participant, Prospective explore will be the sum of the "prospective_explore" column for each participant
# Myopic exploit will be the sum of the "myopic_exploit" column for each participant, Prospective exploit will be the sum of the "prospective_exploit" column for each participant
# Total explore will be the sum of the "total_explore" column for each participant, Total exploit will be the sum of the "total_exploit" column for each participant
# Myopic model-free will be the sum of the "myopic_model-free" column for each participant, Prospective model-free will be the sum of the "prospective_model-free" column for each participant
# Myopic model-based will be the sum of the "myopic_model-based" column for each participant, Prospective model-based will be the sum of the "prospective_model-based" column for each participant
# Total model-free will be the sum of the "total_model-free" column for each participant, Total model-based will be the sum of the "total_model-based" column for each participant
summary_df = df3.groupby('Participant Private ID').agg({
    'money_won': lambda x: x[df3['Trial Number'] == 50].values[0],
    'net_score': lambda x: x[df3['Trial Number'] == 50].values[0],
    'myopic_choice': 'sum',
    'prospective_choice': 'sum',
    'myopic_wins': 'sum',
    'prospective_wins': 'sum',
    'myopic_actions': 'sum',
    'prospective_actions': 'sum',
    'myopic_persistence': 'sum',
    'prospective_persistence': 'sum',
    'myopic_reinforcement': 'sum',
    'prospective_reinforcement': 'sum',
    'myopic_curiosity': 'sum',
    'prospective_curiosity': 'sum',
    'myopic_switch': 'sum',
    'prospective_switch': 'sum',
    'myopic_explore': 'sum',
    'prospective_explore': 'sum',
    'myopic_exploit': 'sum',
    'prospective_exploit': 'sum',
    'total_explore': 'sum',
    'total_exploit': 'sum',
    'myopic_model-free': 'sum',
    'prospective_model-free': 'sum',
    'myopic_model-based': 'sum',
    'prospective_model-based': 'sum',
    'total_model-free': 'sum',
    'total_model-based': 'sum'
}).reset_index()
print(summary_df)

# Save the summary DataFrame to a new Excel file
summary_df.to_excel('win_lose_summary.xlsx', index=False)