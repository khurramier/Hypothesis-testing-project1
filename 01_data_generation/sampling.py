import pandas as pd
import numpy as np

# load branches data from CSV
df=pd.read_csv('02_data/branches_df.csv')
# categorize branches based on student population
df['size_category'] = np.where(df['student_population'] < 150, 'small',
                              np.where(df['student_population'] < 300, 'medium', 'large'))
# make stratum for sampling
df['stratum'] = df['region'] + '_' + df['location'] + '_'+ df['size_category']

# perform stratified sampling: 10% from each stratum
# set seed for reproducibility
np.random.seed(42)

# display stratum counts to calculate porpotinal sample sizes per stratum
stratum_counts = df['stratum'].value_counts()
#print(stratum_counts)

# calculate sample sizes per stratum for strafied sampling
sample_size_per_strtum = {}
for stratum, count in stratum_counts.items():
    sample_size = max(1, int(count/400 * 50))
    sample_size_per_strtum[stratum] = sample_size
total_sampled = sum(sample_size_per_strtum.values())
# counting number of branches less then required size = 50
if total_sampled < 50:
    remaining_required_branches = 50 - total_sampled
print(remaining_required_branches)

# Sample experimental branches
experimental_dfs = []
for str_exp, count_exp in sample_size_per_strtum.items():
    experimental_branches = df[df['stratum']== str_exp]
    sampled_exp = experimental_branches.sample(n=count_exp, random_state=42)
    experimental_dfs.append(sampled_exp)
experimental_sample = pd.concat(experimental_dfs)

# completing the experimental sample to be 50

# Find rows other than those in experimental sample
available_rows = df[~df['branch_code'].isin(experimental_sample['branch_code'])]
# select branches using sampling technique
remaining_exp_branches = available_rows.sample(n=remaining_required_branches, random_state=42)
# add remaining branches to experimental_sample to complete sample of 50 branches
experimental_sample = pd.concat([experimental_sample, remaining_exp_branches])

#Sample for Control Group

# Exclude branches included in experimental sample
df_remaining_after_exp_sample = df[~df['branch_code'].isin(experimental_sample['branch_code'])]

# sample control branches
control_dfs = []
for str_cont, count_cont in sample_size_per_strtum.items():
    control_branches = df_remaining_after_exp_sample[df_remaining_after_exp_sample['stratum']==str_cont]
    sampled_control = control_branches.sample(n=count_cont, random_state=42)
    control_dfs.append(sampled_control)
control_sample = pd.concat(control_dfs)
#control_sample = control_sample.reset_index(drop=True)
# completing the control sample to be 50
available_rows_4_control_sample = df_remaining_after_exp_sample[~df_remaining_after_exp_sample['branch_code'].isin(control_sample['branch_code'])]
remaining_contorl_branches= available_rows_4_control_sample.sample(n=remaining_required_branches, random_state=42)
control_sample = pd.concat([control_sample, remaining_contorl_branches])

#reset indecies of experimental and control sample dataframes
experimental_sample= experimental_sample.reset_index(drop=True)
print(experimental_sample)

control_sample = control_sample.reset_index(drop=True)
print(control_sample)

# Update branches dataframe with column study_group

#make dataframe of 'branches not selected' in exp/cont groups
df_remaining_rows_after_sampling = available_rows_4_control_sample[~available_rows_4_control_sample['branch_code'].isin(control_sample['branch_code'])]
print(len(df_remaining_rows_after_sampling))

# adding study_group columns to experimental/conrol sample and 'branches not selected'
experimental_sample['study_group'] = 'experimental'
control_sample['study_group'] = 'control'
df_remaining_rows_after_sampling['study_group'] = 'not selected'
branches_with_study_groups = pd.concat([experimental_sample, control_sample, df_remaining_rows_after_sampling])
print(branches_with_study_groups.tail())
branches_with_study_groups.to_csv('02_data/branches_with_study_groups.csv', index=False)
print(branches_with_study_groups['study_group'].value_counts())