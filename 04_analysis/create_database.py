import sqlite3 
import pandas as pd

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
# Print count of records loaded
print(f'{len(metrics)} performance records loaded')

# Verify tables were created
print("\nVerifying tables...")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f'\nTables created {[t[0] for t in tables]}\n')
print('Branches Table\n')
sample_branches = pd.read_sql("SELECT * FROM branches LIMIT 5", conn)
print(sample_branches)
print('\nPerformance Metrics Table\n')
sample_metrics = pd.read_sql('SELECT * FROM metrics LIMIT 5', conn)
print(sample_metrics)
# Commit (not strictly necessary for reads, but good practice) and close connection
conn.commit()
conn.close()

      