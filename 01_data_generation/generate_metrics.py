import pandas as pd
import numpy as np

# Insert seed for randomness
np.random.seed(42)

#Import data
df= pd.read_csv('02_data/branches_with_study_groups.csv')

#Genrate base line metrics
baseline_metrics = []

# Extract branch code and population from df
for _, branch in df.iterrows():
    branch_code = branch['branch_code']
    student_population = branch['student_population']
# Create base line data
    baseline_metrics.append({
        'branch_code': branch_code,
        'measurement_period': 'baseline',

        #Create pass percentage using normal distribution because:
        #pass percentage revolves around a mean with some sd
        'pass_percentage': round(np.clip(np.random.normal(70, 5), 0, 100),2), #percentage remains between 0 and 100
        
        #Create new_enrollments using poisson distribution  because:
        # new enrollments are discreate and
        #usually occur at a smooth rate (but randomly) w.r.t. current students' population
        'new_enrollments': int(np.random.poisson(0.3 * student_population)),

        #Create revenue for branches using lognormal distribution because:
        #Revenue cant be negative, it is right skewed, some branches make much more revenue than others
        'revenue': round(np.random.lognormal(np.log(student_population*500), 0.15),2),
        
        #Create cleanliness score using uniform distribution because:
        #Cleanliness level of most of the branches remains around average
        'cleanliness_score': round(np.clip(np.random.normal(60, 10), 30, 100),2), # usually not less than 30 and more than 100
        
        'measurement_date': '2023-01-01'
    })
# Convert in dataframe
baseline_df =pd.DataFrame(baseline_metrics)

# Genrate metrics when branches assessed after 1 year
# Different improvements based on study groups 
year1_metrics = []

for _, branch in df.iterrows():
    branch_code = branch['branch_code']
    study_group = branch['study_group']

    # Get baseline values for branch 
    baseline = baseline_df[baseline_df['branch_code'] == branch_code].iloc[0]

    # Different improvement based on study group
    if study_group == 'experimental':
        pass_improvement = np.random.uniform(6, 10)
        enroll_growth = np.random.uniform(1.1, 1.2)  # 10% to 20% growth
        revenue_growth = np.random.uniform(1.08, 1.15)  # 8% to 15% growth
        clean_improvement = np.random.uniform(8, 12)

    elif study_group == 'control':
        pass_improvement = np.random.uniform(1, 3)
        enroll_growth = np.random.uniform(1.0, 1.05)  # 0% to 5% growth
        revenue_growth = np.random.uniform(1.01, 1.05)  # 1% to 5% growth
        clean_improvement = np.random.uniform(1, 3)

    else: # for branches not selected
        pass_improvement = np.random.uniform(1, 4)
        enroll_growth = np.random.uniform(1.0, 1.06)  # 0% to 6% growth
        revenue_growth = np.random.uniform(1.02, 1.06)  # 2% to 6% growth
        clean_improvement = np.random.uniform(1, 4)

# Calculate year 1 values
    year1_metrics.append({
        'branch_code' : branch['branch_code'],
        'measurement_period' : 'year 1',
        'pass_percentage': round(min(100, baseline['pass_percentage'] + pass_improvement), 2),
        'new_enrollments': int(baseline['new_enrollments'] * enroll_growth),
        'revenue': round(baseline['revenue'] * revenue_growth, 2),
        'cleanliness_score': round(min(100, baseline['cleanliness_score'] + clean_improvement), 2),
        'measurement_date': '2024-01-01'
    })
year1_df = pd.DataFrame(year1_metrics)
print(year1_df.head())
print(f'{len(year1_df)} records generated')

# combining and saving files
all_metrics = pd.concat([baseline_df, year1_df], ignore_index=True)
year1_df.to_csv('02_data/year1_df.csv', index=False)
all_metrics.to_csv('02_data/all_metrics.csv', index=False)

print("\n" + "="*60)
print("✓ METRICS GENERATED SUCCESSFULLY!")
print("="*60)
print(f"Files created:")
print(f"  - 02_data/baseline_metrics.csv ({len(baseline_df)} records)")
print(f"  - 02_data/year1_metrics.csv ({len(year1_df)} records)")
print(f"  - 02_data/all_metrics.csv ({len(all_metrics)} records)")

# Merge with branches to compare groups for testing data
test = year1_df.merge(df[['branch_code', 'study_group']], on='branch_code')
# comparing pass percentage
print (f'\n\nPass Percentage Comparison\n ={"="*30}')
print(test.groupby('study_group')['pass_percentage'].mean())
# comparing new enrollments
print(f'\nNew Enrollment Comparison\n {"="*30}')
print(test.groupby('study_group')['new_enrollments'].mean())
# comparing revenue
print(f'\nRevenue Comparison\n {"="*30}')
print(test.groupby('study_group')['revenue'].mean())
#comparing cleanliness score
print(f'\nCleanliness Score Comparison\n {"="*30}')
print(test.groupby('study_group')['cleanliness_score'].mean())