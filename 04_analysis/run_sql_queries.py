import sqlite3
import pandas as pd

# connet to database
conn= sqlite3.connect('02_data/branches_df.db')

# create heading
print(f'{'*'*30}\n')
print('SQL Analysis Queries')
print(f'\n{'*'*30}\n')

# ===== QUERY 1: Study Group Distribution =====
print("\n" + "-"*70)
print("QUERY 1: Study Group Distribution")
print("-"*70)

query1 = """
SELECT 
    study_group,
    COUNT(*) AS count
FROM branches
GROUP BY study_group
ORDER BY count DESC;
"""
result1 = pd.read_sql(query1, conn)
print(result1)

# ===== QUERY 2: Baseline Balance Check =====
print("\n" + "-"*70)
print("QUERY 2: Baseline Balance Check (Are groups similar at start?)")
print("-"*70)

query2 = """
SELECT
    b.study_group,
    COUNT(*) AS n_branches,
    ROUND(AVG(m.pass_percentage),2) AS Bsl_pass_percentage,
    ROUND(AVG(m.new_enrollments),2) AS Bsl_new_enrollments,
    ROUND(AVG(m.revenue),2) AS Bsl_revenue,
    ROUND(AVG(m.cleanliness_score),2) AS Bsl_cleanliness_score
FROM branches as b
JOIN metrics as m ON b.branch_code = m.branch_code
WHERE m.measurement_period = 'baseline'
    AND b.study_group IN('experimental', 'control')
GROUP BY b.study_group
"""
result2 = pd.read_sql(query2, conn)
print(result2)

# ===== QUERY 3: Performance After 1 Year =====
print("\n" + "-"*70)
print("QUERY 3: Performace After 1 Year")
print("-"*70)

query3 = """
SELECT
    b.study_group,
    COUNT(*) AS n_branches,
    ROUND(AVG(m.pass_percentage),2) AS Y1_pass_percentage,
    ROUND(AVG(m.new_enrollments),2) AS Y1_new_enrollments,
    ROUND(AVG(m.revenue),2) AS Y1_revenue,
    ROUND(AVG(m.cleanliness_score),2) AS Y1_cleanliness_score
FROM branches as b
JOIN metrics as m ON b.branch_code = m.branch_code
WHERE m.measurement_period = 'year 1'
    AND b.study_group IN('experimental', 'control')
GROUP BY b.study_group
"""
result3 = pd.read_sql(query3, conn)
print(result3)

# ===== QUERY 4: Calculate Improvements =====
print("\n" + "-"*70)
print("QUERY 4: Calculating Improvements (Year 1 vs Baseline)")
print("-"*70)

query4 = """
WITH 
    baseline AS (
SELECT 
    branch_code,
    pass_percentage AS base_pass,
    new_enrollments AS base_enroll,
    revenue AS base_revenue,
    cleanliness_score AS base_cleanliness
FROM metrics
WHERE measurement_period = 'baseline'
),

    year1 AS (
SELECT 
    branch_code,
    pass_percentage AS y1_pass,
    new_enrollments AS y1_enroll,
    revenue AS y1_revenue,
    cleanliness_score AS y1_cleanliness
FROM metrics
WHERE measurement_period = 'year 1'
)
SELECT 
    b.branch_code,
    b.study_group,
    (y.y1_pass - bl.base_pass) AS pass_improvement,
    ROUND(CAST((y.y1_enroll - bl.base_enroll) AS FLOAT) * 100.0 / bl.base_enroll, 2) AS enrollment_growth,
    ROUND((y.y1_revenue - bl.base_revenue) * 100.0 / bl.base_revenue, 2) AS revenue_growth,
    (y1_cleanliness- base_cleanliness) AS cleanliness_improvement
FROM branches AS b
JOIN baseline As bl ON b.branch_code = bl.branch_code
JOIN year1 As y ON b.branch_code = y.branch_code
WHERE b.study_group IN ('experimental', 'control')
"""

result4 = pd.read_sql(query4, conn)
print(f"Calculated improvements for {len(result4)} branches")
print("\nSample improvements:")
print(result4.head(10))

# Save improvements to CSV for next step
result4.to_csv('02_data/improvements.csv', index=False)
print(f"\n Saved to: 02_data/improvements.csv")

# ===== QUERY 5: Average Improvements by Group =====
print("\n" + "-"*70)
print("QUERY 5: Average Improvements by Group")
print("-"*70)

query5 = """
WITH 
    baseline AS (
SELECT 
    branch_code,
    pass_percentage AS base_pass,
    new_enrollments AS base_enroll,
    revenue AS base_revenue,
    cleanliness_score AS base_cleanliness
FROM metrics
WHERE measurement_period = 'baseline'
),

    year1 AS (
SELECT 
    branch_code,
    pass_percentage AS y1_pass,
    new_enrollments AS y1_enroll,
    revenue AS y1_revenue,
    cleanliness_score AS y1_cleanliness
FROM metrics
WHERE measurement_period = 'year 1'
)
SELECT 
    b.study_group,
    COUNT(*) AS n_branches,
    (y.y1_pass - bl.base_pass) AS pass_improvement,
    ROUND(CAST((y.y1_enroll - bl.base_enroll) AS FLOAT) * 100.0 / bl.base_enroll, 2) AS enrollment_growth,
    ROUND((y.y1_revenue - bl.base_revenue) * 100.0 / bl.base_revenue, 2) AS revenue_growth,
    (y.y1_cleanliness - bl.base_cleanliness) AS cleanliness_improvement
FROM branches AS b
JOIN baseline As bl ON b.branch_code = bl.branch_code
JOIN year1 As y ON b.branch_code = y.branch_code
WHERE b.study_group IN ('experimental', 'control')
GROUP BY b.study_group
"""
result5 = pd.read_sql(query5, conn)
print(result5)

#close database connection
conn.close()

print(f'\n\n{'*' * 70}\n')
print(f'SQl Analysis Completed')
print(f'\n{'*' * 70}\n')