import pandas as pd
import numpy as np

#setting random seed for reproducibility
np.random.seed(42)

#generate 400 branches using function
def generate_branches (n=400):

    #create empty list to hold branch data
    branches =[]

    #generate branch data using loop
    for i in range(1, n+1):

        #branch codes from B001 to B400
        branch_code = f"B{i:03d}" 

        #randomly assign location
        location = pd.Series(np.random.choice(['rural', 'urban'])) 

        #randomly assign student population. less for rural, more for urban
        if(location[0] == 'rural'): 
            student_population = pd.Series(np.random.randint(50, 200))
        else:
            student_population = pd.Series(np.random.randint(100, 500))
        #randomly assign region
        region = pd.Series(np.random.choice(['Punjab', 'KPK', 'Sind', 'Balochistan']))
        #establinhment year between 2010-2020
        establishment_year = np.random.randint(2010, 2020)
        #append branch data to list    
        branches.append({'branch_code': branch_code, 'location': location[0], 'student_population': student_population[0], 'region': region[0], 'establishment_year': establishment_year})
    return pd.DataFrame(branches)
branches_df = generate_branches()   
print("Branches DataFrame:")
print(branches_df.head(10))
branches_df.to_csv('02_data/branches_df.csv', index=False)
     