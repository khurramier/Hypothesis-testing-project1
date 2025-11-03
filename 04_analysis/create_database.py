import sqlite3 
import pandas as pd
import os
# Create header
print("="*60)
print("CREATING SQLITE DATABASE")
print("="*60)

# Create database connection
conn = sqlite3.connect('02_data/branches_df.db')
print("Database connection created\n")

# Load branches data
print('Loading branches data\n')
branches = pd.read_csv('02_data/branches_with_study_groups.csv')
branches.to_sql('branches', conn, if_exists='replace', index=False)
print(f'{len(branches)} branches loaded')

# Load metric data
print('Loading performance data\n')
metrics = pd.read_csv('02_data/all_metrics.csv')
metrics.to_sql('metrics', conn, if_exists='replace', index=False)
print(f'{len(metrics)} performance records loaded')

