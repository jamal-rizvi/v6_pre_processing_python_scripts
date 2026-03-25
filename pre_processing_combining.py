import numpy as np
import pandas as pd
import os

# Read the Excel file into a variable
gorilla_data = os.path.dirname(os.path.abspath(__file__))
ww = pd.read_excel(os.path.join(gorilla_data, 'win_win_summary.xlsx'))
wl = pd.read_excel(os.path.join(gorilla_data, 'win_lose_summary.xlsx'))
lw = pd.read_excel(os.path.join(gorilla_data, 'lose_win_summary.xlsx'))
ll = pd.read_excel(os.path.join(gorilla_data, 'lose_lose_summary.xlsx'))
igt = pd.read_excel(os.path.join(gorilla_data, 'igt_control_summary.xlsx'))
sot = pd.read_excel(os.path.join(gorilla_data, 'sot_control_summary.xlsx'))
questionnaire = pd.read_excel(os.path.join(gorilla_data, 'questionnaire_summary.xlsx'))
discounting = pd.read_excel(os.path.join(gorilla_data, 'delay_discounting_k_median.xlsx'))
ssrt = pd.read_excel(os.path.join(gorilla_data, 'stop_signal_SSRT.xlsx'))

# Create a new dataframe to store the combined data
# Only take the "Participant Private ID", "money_won", 
# Title each column based on the name of the variable and the DV, for example "money_won_win_win", "money_won_win_lose", "money_won_lose_win", "money_won_lose_lose", "money_won_igt_control", "money_won_sot_control"
combined_df = pd.DataFrame()
combined_df['Participant Private ID'] = ww['Participant Private ID']
combined_df['money_won_win_win'] = ww['money_won']
combined_df['money_won_win_lose'] = wl['money_won']
combined_df['money_won_lose_win'] = lw['money_won']
combined_df['money_won_lose_lose'] = ll['money_won']
combined_df['money_won_igt_control'] = igt['money_won']
combined_df['money_won_sot_control'] = sot['money_won']


# Append additional columns for "net_score", "myopic_choice", "prospective_choice", "myopic_wins", "prospective_wins" from each dataframe, with the same naming convention as above
combined_df['net_score_win_win'] = ww['net_score']
combined_df['net_score_win_lose'] = wl['net_score']
combined_df['net_score_lose_win'] = lw['net_score']
combined_df['net_score_lose_lose'] = ll['net_score']
combined_df['net_score_igt_control'] = igt['net_score']
combined_df['net_score_sot_control'] = sot['net_score']
combined_df['delay_discounting_rate'] = discounting['discount_rate']
combined_df['SSRT'] = ssrt['SSRT']
combined_df['myopic_choice_win_win'] = ww['myopic_choice']
combined_df['myopic_choice_win_lose'] = wl['myopic_choice']
combined_df['myopic_choice_lose_win'] = lw['myopic_choice']
combined_df['myopic_choice_lose_lose'] = ll['myopic_choice']
combined_df['prospective_choice_win_win'] = ww['prospective_choice']
combined_df['prospective_choice_win_lose'] = wl['prospective_choice']
combined_df['prospective_choice_lose_win'] = lw['prospective_choice']
combined_df['prospective_choice_lose_lose'] = ll['prospective_choice']
combined_df['myopic_wins_win_win'] = ww['myopic_wins']
combined_df['myopic_wins_win_lose'] = wl['myopic_wins']
combined_df['myopic_wins_lose_win'] = lw['myopic_wins']
combined_df['myopic_wins_lose_lose'] = ll['myopic_wins']
combined_df['prospective_wins_win_win'] = ww['prospective_wins']
combined_df['prospective_wins_win_lose'] = wl['prospective_wins']
combined_df['prospective_wins_lose_win'] = lw['prospective_wins']
combined_df['prospective_wins_lose_lose'] = ll['prospective_wins']

#Append additional columns for "healthy_living_full_score", "exercise", "healthy_food", "saving_money", "sleep", "smoking", "unhealthy_food", "drinking", "spending_money" from the questionnaire dataframe, with the same naming convention as above
combined_df['healthy_living_full_score'] = questionnaire['healthy_living_full_score']
combined_df['exercise'] = questionnaire['exercise'] 
combined_df['healthy_food'] = questionnaire['healthy_food']
combined_df['saving_money'] = questionnaire['saving_money']
combined_df['sleep'] = questionnaire['sleep']
combined_df['smoking'] = questionnaire['smoking']
combined_df['unhealthy_food'] = questionnaire['unhealthy_food']
combined_df['drinking'] = questionnaire['drinking']
combined_df['spending_money'] = questionnaire['spending_money']

# Save the combined dataframe to a new Excel file
combined_df.to_excel('combined_summary.xlsx', index=False)


# Create new dataframe to store the combined data vertically
# The new df will have columns for "participant", "task", total_money_won", "net_score"
# The data frame will be populated one variable at a time, e.g. "ww" first, then "wl", then "lw", then "ll", then "igt_control", then "sot_control"
# The participant column will be populated with the "Participant Private ID" column from each dataframe, the task column will be populated with the name of the task (e.g. "win_win", "win_lose", "lose_win", "lose_lose", "igt_control", "sot_control"), the total_money_won column will be populated with the "money_won" column from each dataframe, and the net_score column will be populated with the "net_score" column from each dataframe
combined_df_long = pd.DataFrame()
for df, task in zip([ww, wl, lw, ll, igt, sot], ['win_win', 'win_lose', 'lose_win', 'lose_lose', 'igt_control', 'sot_control']):
    temp_df = pd.DataFrame()
    temp_df['participant'] = df['Participant Private ID']
    temp_df['task'] = task
    temp_df['total_money_won'] = df['money_won']
    temp_df['net_score'] = df['net_score']
    combined_df_long = pd.concat([combined_df_long, temp_df], ignore_index=True)

# Then two additional columns will be added to the long df, one for "Now" and one for "Later",
# The following rules will be applied to populate the "Now" and "Later" columns:
# If task is "win_win" then "Now" will be populated with "Win" and "Later" will be populated with "Win",
# If task is "win_lose" then "Now" will be populated with "Win" and "Later" will be populated with "Lose",
# If task is "lose_win" then "Now" will be populated with "Lose" and "Later" will be populated with "Win",
# If task is "lose_lose" then "Now" will be populated with "Lose" and "Later" will be populated with "Lose",
# If task is "igt_control" then "Now" will be populated with "None" and "Later" will be populated with "Both",
# If task is "sot_control" then "Now" will be populated with "Both" and "Later" will be populated with "None", 
combined_df_long['Now'] = np.where(combined_df_long['task'] == 'win_win', 'Win',
                                np.where(combined_df_long['task'] == 'win_lose', 'Win',
                                         np.where(combined_df_long['task'] == 'lose_win', 'Lose',
                                                  np.where(combined_df_long['task'] == 'lose_lose', 'Lose',
                                                           np.where(combined_df_long['task'] == 'igt_control', 'None',
                                                                    np.where(combined_df_long['task'] == 'sot_control', 'Both', ''))))))
combined_df_long['Later'] = np.where(combined_df_long['task'] == 'win_win', 'Win',
                                np.where(combined_df_long['task'] == 'win_lose', 'Lose',
                                            np.where(combined_df_long['task'] == 'lose_win', 'Win',
                                                    np.where(combined_df_long['task'] == 'lose_lose', 'Lose',
                                                            np.where(combined_df_long['task'] == 'igt_control', 'Both',
                                                                        np.where(combined_df_long['task'] == 'sot_control', 'None', ''))))))

# Save the long format combined dataframe to a new Excel file
combined_df_long.to_excel('combined_summary_long_6_tasks.xlsx', index=False)


# Create new dataframe to store the combined data vertically
# The new df will have columns for "participant", "task", "myopic_choice", "prospective_choice", "myopic_wins", "prospective_wins", "myopic_actions", "prospective_actions", "myopic_persistence", "prospective_persistence", "myopic_reinforcement", "prospective_reinforcement", "myopic_curiosity", "prospective_curiosity", "myopic_switch", "prospective_switch", "myopic_explore", "prospective_explore", "myopic_exploit", "prospective_exploit", "total_explore", "total_exploit", "myopic_model-free", "prospective_model-free", "myopic_model-based", "prospective_model-based", "total_model-free", "total_model-based"
# The data frame will be populated one variable at a time, e.g. "ww" first, then "wl", then "lw", then "ll"
# The participant column will be populated with the "Participant Private ID" column from each dataframe, the task column will be populated with the name of the task (e.g. "win_win", "win_lose", "lose_win", "lose_lose", "igt_control", "sot_control"), the "myopic_choice" column will be populated with the "myopic_choice" column from each dataframe, the "prospective_choice" column will be populated with the "prospective_choice" column from each dataframe, the "myopic_wins" column will be populated with the "myopic_wins" column from each dataframe, and the "prospective_wins" column will be populated with the "prospective_wins" column from each dataframe
# The "myopic_actions" column will be populated with the "myopic_actions" column from each dataframe, the "prospective_actions" column will be populated with the "prospective_actions" column from each dataframe, the "myopic_persistence" column will be populated with the "myopic_persistence" column from each dataframe, the "prospective_persistence" column will be populated with the "prospective_persistence" column from each dataframe, the "myopic_reinforcement" column will be populated with the "myopic_reinforcement" column from each dataframe, the "prospective_reinforcement" column will be populated with the "prospective_reinforcement" column from each dataframe, the "myopic_curiosity" column will be populated with the "myopic_curiosity" column from each dataframe, the "prospective_curiosity" column will be populated with the "prospective_curiosity" column from each dataframe, the "myopic_switch" column will be populated with the "myopic_switch" column from each dataframe, the "prospective_switch" column will be populated with the "prospective_switch" column from each dataframe, the "myopic_explore" column will be populated with the "myopic_explore" column from each dataframe, and the "prospective_explore" column will be populated with the "prospective_explore" column from each dataframe
# The "total_explore" column will be the sum of the "myopic_explore" and "prospective_explore" columns for each participant, the "total_exploit" column will be the sum of the "myopic_exploit" and "prospective_exploit" columns for each participant, the "myopic_model-free" column will be the sum of the "myopic_model-free" column for each participant, the "prospective_model-free" column will be the sum of the "prospective_model-free" column for each participant, the "myopic_model-based" column will be the sum of the "myopic_model-based" column for each participant, the "prospective_model-based" column will be the sum of the "prospective_model-based" column for each participant, the "total_model-free" column will be the sum of the "total_model-free" column for each participant, and the "total_model-based" column will be the sum of the "total_model-based" column for each participant

combined_df_long_choices = pd.DataFrame()
for df, task in zip([ww, wl, lw, ll], ['win_win', 'win_lose', 'lose_win', 'lose_lose']):
    temp_df = pd.DataFrame()
    temp_df['participant'] = df['Participant Private ID']
    temp_df['task'] = task
    temp_df['myopic_choice'] = df['myopic_choice']
    temp_df['prospective_choice'] = df['prospective_choice']
    temp_df['myopic_wins'] = df['myopic_wins']
    temp_df['prospective_wins'] = df['prospective_wins']
    temp_df['myopic_actions'] = df['myopic_actions']
    temp_df['prospective_actions'] = df['prospective_actions']
    temp_df['myopic_persistence'] = df['myopic_persistence']
    temp_df['prospective_persistence'] = df['prospective_persistence']
    temp_df['myopic_reinforcement'] = df['myopic_reinforcement']
    temp_df['prospective_reinforcement'] = df['prospective_reinforcement']
    temp_df['myopic_curiosity'] = df['myopic_curiosity']
    temp_df['prospective_curiosity'] = df['prospective_curiosity']
    temp_df['myopic_switch'] = df['myopic_switch']
    temp_df['prospective_switch'] = df['prospective_switch']
    temp_df['myopic_explore'] = df['myopic_explore']
    temp_df['prospective_explore'] = df['prospective_explore']
    temp_df['total_explore'] = df['total_explore']
    temp_df['total_exploit'] = df['total_exploit']
    temp_df['myopic_model-free'] = df['myopic_model-free']
    temp_df['prospective_model-free'] = df['prospective_model-free']
    temp_df['myopic_model-based'] = df['myopic_model-based']
    temp_df['prospective_model-based'] = df['prospective_model-based']
    temp_df['total_model-free'] = df['total_model-free']
    temp_df['total_model-based'] = df['total_model-based']
    combined_df_long_choices = pd.concat([combined_df_long_choices, temp_df], ignore_index=True)

# Then two additional columns will be added to the long df, one for "Now" and one for "Later",
# The following rules will be applied to populate the "Now" and "Later" columns:
# If task is "win_win" then "Now" will be populated with "Win" and "Later" will be populated with "Win",
# If task is "win_lose" then "Now" will be populated with "Win" and "Later" will be populated with "Lose",
# If task is "lose_win" then "Now" will be populated with "Lose" and "Later" will be populated with "Win",
# If task is "lose_lose" then "Now" will be populated with "Lose" and "Later" will be populated with "Lose",
combined_df_long_choices['Now'] = np.where(combined_df_long_choices['task'] == 'win_win', 'Win',
                                np.where(combined_df_long_choices['task'] == 'win_lose', 'Win',
                                         np.where(combined_df_long_choices['task'] == 'lose_win', 'Lose',
                                                  np.where(combined_df_long_choices['task'] == 'lose_lose', 'Lose', ''))))
combined_df_long_choices['Later'] = np.where(combined_df_long_choices['task'] == 'win_win', 'Win',
                                np.where(combined_df_long_choices['task'] == 'win_lose', 'Lose',
                                            np.where(combined_df_long_choices['task'] == 'lose_win', 'Win',
                                                    np.where(combined_df_long_choices['task'] == 'lose_lose', 'Lose', ''))))

# Move the columns "Now" and "Later" to be after the "task" column
cols = combined_df_long_choices.columns.tolist()
cols.insert(cols.index('task') + 1, cols.pop(cols.index('Now')))
cols.insert(cols.index('task') + 2, cols.pop(cols.index('Later')))
combined_df_long_choices = combined_df_long_choices[cols]

# Save the long format combined dataframe to a new Excel file
combined_df_long_choices.to_excel('combined_summary_long_4_tasks.xlsx', index=False)


# Read combined data from the Excel file into a new variable
expanded_data = pd.read_excel(os.path.join(gorilla_data, 'combined_summary.xlsx'))

# Append additional columns for "myopic_actions", "prospective_actions", "myopic_persistence", "prospective_persistence", "myopic_reinforcement", "prospective_reinforcement", "myopic_curiosity", "prospective_curiosity", "myopic_switch", "prospective_switch", "myopic_explore", "prospective_explore", "total_explore", "total_exploit", "myopic_model-free", "prospective_model-free", "myopic_model-based", "prospective_model-based", "total_model-free", "total_model-based" from each dataframe, with the same naming convention as above
expanded_data['myopic_actions_win_win'] = ww['myopic_actions']
expanded_data['myopic_actions_win_lose'] = wl['myopic_actions']
expanded_data['myopic_actions_lose_win'] = lw['myopic_actions']
expanded_data['myopic_actions_lose_lose'] = ll['myopic_actions']
expanded_data['prospective_actions_win_win'] = ww['prospective_actions']
expanded_data['prospective_actions_win_lose'] = wl['prospective_actions']
expanded_data['prospective_actions_lose_win'] = lw['prospective_actions']
expanded_data['prospective_actions_lose_lose'] = ll['prospective_actions']
expanded_data['myopic_persistence_win_win'] = ww['myopic_persistence']
expanded_data['myopic_persistence_win_lose'] = wl['myopic_persistence']
expanded_data['myopic_persistence_lose_win'] = lw['myopic_persistence']
expanded_data['myopic_persistence_lose_lose'] = ll['myopic_persistence']
expanded_data['prospective_persistence_win_win'] = ww['prospective_persistence']
expanded_data['prospective_persistence_win_lose'] = wl['prospective_persistence']
expanded_data['prospective_persistence_lose_win'] = lw['prospective_persistence']
expanded_data['prospective_persistence_lose_lose'] = ll['prospective_persistence']
expanded_data['myopic_reinforcement_win_win'] = ww['myopic_reinforcement']
expanded_data['myopic_reinforcement_win_lose'] = wl['myopic_reinforcement']
expanded_data['myopic_reinforcement_lose_win'] = lw['myopic_reinforcement']
expanded_data['myopic_reinforcement_lose_lose'] = ll['myopic_reinforcement']
expanded_data['prospective_reinforcement_win_win'] = ww['prospective_reinforcement']
expanded_data['prospective_reinforcement_win_lose'] = wl['prospective_reinforcement']
expanded_data['prospective_reinforcement_lose_win'] = lw['prospective_reinforcement']
expanded_data['prospective_reinforcement_lose_lose'] = ll['prospective_reinforcement']
expanded_data['myopic_curiosity_win_win'] = ww['myopic_curiosity']    
expanded_data['myopic_curiosity_win_lose'] = wl['myopic_curiosity']
expanded_data['myopic_curiosity_lose_win'] = lw['myopic_curiosity']
expanded_data['myopic_curiosity_lose_lose'] = ll['myopic_curiosity']
expanded_data['prospective_curiosity_win_win'] = ww['prospective_curiosity']
expanded_data['prospective_curiosity_win_lose'] = wl['prospective_curiosity']
expanded_data['prospective_curiosity_lose_win'] = lw['prospective_curiosity']
expanded_data['prospective_curiosity_lose_lose'] = ll['prospective_curiosity']
expanded_data['myopic_switch_win_win'] = ww['myopic_switch']
expanded_data['myopic_switch_win_lose'] = wl['myopic_switch']
expanded_data['myopic_switch_lose_win'] = lw['myopic_switch']
expanded_data['myopic_switch_lose_lose'] = ll['myopic_switch']
expanded_data['prospective_switch_win_win'] = ww['prospective_switch']
expanded_data['prospective_switch_win_lose'] = wl['prospective_switch']
expanded_data['prospective_switch_lose_win'] = lw['prospective_switch']
expanded_data['prospective_switch_lose_lose'] = ll['prospective_switch']
expanded_data['myopic_explore_win_win'] = ww['myopic_explore']
expanded_data['myopic_explore_win_lose'] = wl['myopic_explore']
expanded_data['myopic_explore_lose_win'] = lw['myopic_explore']
expanded_data['myopic_explore_lose_lose'] = ll['myopic_explore']
expanded_data['prospective_explore_win_win'] = ww['prospective_explore']
expanded_data['prospective_explore_win_lose'] = wl['prospective_explore']
expanded_data['prospective_explore_lose_win'] = lw['prospective_explore']
expanded_data['prospective_explore_lose_lose'] = ll['prospective_explore']
expanded_data['myopic_exploit_win_win'] = ww['myopic_exploit']
expanded_data['myopic_exploit_win_lose'] = wl['myopic_exploit']
expanded_data['myopic_exploit_lose_win'] = lw['myopic_exploit']
expanded_data['myopic_exploit_lose_lose'] = ll['myopic_exploit']
expanded_data['prospective_exploit_win_win'] = ww['prospective_exploit']
expanded_data['prospective_exploit_win_lose'] = wl['prospective_exploit']
expanded_data['prospective_exploit_lose_win'] = lw['prospective_exploit']
expanded_data['prospective_exploit_lose_lose'] = ll['prospective_exploit']
expanded_data['total_explore_win_win'] = ww['total_explore']
expanded_data['total_explore_win_lose'] = wl['total_explore']
expanded_data['total_explore_lose_win'] = lw['total_explore']
expanded_data['total_explore_lose_lose'] = ll['total_explore']
expanded_data['total_exploit_win_win'] = ww['total_exploit']
expanded_data['total_exploit_win_lose'] = wl['total_exploit']
expanded_data['total_exploit_lose_win'] = lw['total_exploit']
expanded_data['total_exploit_lose_lose'] = ll['total_exploit']
expanded_data['myopic_model_free_win_win'] = ww['myopic_model-free']
expanded_data['myopic_model_free_win_lose'] = wl['myopic_model-free']
expanded_data['myopic_model_free_lose_win'] = lw['myopic_model-free']
expanded_data['myopic_model_free_lose_lose'] = ll['myopic_model-free']
expanded_data['prospective_model_free_win_win'] = ww['prospective_model-free']
expanded_data['prospective_model_free_win_lose'] = wl['prospective_model-free']
expanded_data['prospective_model_free_lose_win'] = lw['prospective_model-free']
expanded_data['prospective_model_free_lose_lose'] = ll['prospective_model-free']
expanded_data['myopic_model_based_win_win'] = ww['myopic_model-based']
expanded_data['myopic_model_based_win_lose'] = wl['myopic_model-based']   
expanded_data['myopic_model_based_lose_win'] = lw['myopic_model-based']
expanded_data['myopic_model_based_lose_lose'] = ll['myopic_model-based']
expanded_data['prospective_model_based_win_win'] = ww['prospective_model-based']
expanded_data['prospective_model_based_win_lose'] = wl['prospective_model-based']
expanded_data['prospective_model_based_lose_win'] = lw['prospective_model-based']
expanded_data['prospective_model_based_lose_lose'] = ll['prospective_model-based']
expanded_data['total_model_free_win_win'] = ww['total_model-free']
expanded_data['total_model_free_win_lose'] = wl['total_model-free']
expanded_data['total_model_free_lose_win'] = lw['total_model-free']
expanded_data['total_model_free_lose_lose'] = ll['total_model-free']
expanded_data['total_model_based_win_win'] = ww['total_model-based']
expanded_data['total_model_based_win_lose'] = wl['total_model-based']
expanded_data['total_model_based_lose_win'] = lw['total_model-based']
expanded_data['total_model_based_lose_lose'] = ll['total_model-based']

print(expanded_data)

# Save the expanded dataframe to a new Excel file
expanded_data.to_excel('expanded_combined_summary.xlsx', index=False)