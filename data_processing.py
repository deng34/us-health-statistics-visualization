import pandas as pd
import numpy as np

# Define column specifications (start, end)
# Note: Column indices are 0-based and the end index is exclusive.
column_specs = [
(0, 2), # _STATE
(177, 178), # SEXVAR
(79, 80), # GENHLTH
(94, 95), # CVDCRHD4
(95, 96), # CVDSTRK3
(99, 100), # CHCOCNC1
(101, 102), # HAVARTH4
(2007, 2016) # _LLCPWT
]

# Define column names corresponding to the specifications
column_names = [
'_STATE', # State FIPS Code
'SEXVAR', # Sex of Respondent
'GENHLTH', # General Health
'CVDCRHD4', # Ever Diagnosed with Angina or Coronary Heart Disease
'CVDSTRK3', # Ever Diagnosed with a Stroke
'CHCOCNC1', # Ever Diagnosed with Melanoma or Any Other Types of Cancer
'HAVARTH4', # Told Had Arthritis
'_LLCPWT' # Final Weight: Land-line and Cell-phone Data
]

df = pd.read_fwf(
r'path/to/your/file/LLCP2014.ASC',
colspecs=column_specs,
names=column_names,
dtype={
'_STATE': 'float64',
'SEXVAR': 'float64',
'GENHLTH': 'float64',
'CVDCRHD4': 'float64',
'CVDSTRK3': 'float64',
'CHCOCNC1': 'float64',
'HAVARTH4': 'float64',
'_LLCPWT': 'float64'
},
na_values=['', ' '],
keep_default_na=True,
encoding='latin1'
)


# Define mapping dictionaries
# State FIPS Code Mapping
state_codes = {
1: 'Alabama', 2: 'Alaska', 4: 'Arizona', 5: 'Arkansas',
6: 'California', 8: 'Colorado', 9: 'Connecticut', 10: 'Delaware',
11: 'District of Columbia', 12: 'Florida', 13: 'Georgia', 15: 'Hawaii',
16: 'Idaho', 17: 'Illinois', 18: 'Indiana', 19: 'Iowa',
20: 'Kansas', 21: 'Kentucky', 22: 'Louisiana', 23: 'Maine',
24: 'Maryland', 25: 'Massachusetts', 26: 'Michigan', 27: 'Minnesota',
28: 'Mississippi', 29: 'Missouri', 30: 'Montana', 31: 'Nebraska',
32: 'Nevada', 33: 'New Hampshire', 34: 'New Jersey', 35: 'New Mexico',
36: 'New York', 37: 'North Carolina', 38: 'North Dakota', 39: 'Ohio',
40: 'Oklahoma', 41: 'Oregon', 42: 'Pennsylvania', 44: 'Rhode Island',
45: 'South Carolina', 46: 'South Dakota', 47: 'Tennessee', 48: 'Texas',
49: 'Utah', 50: 'Vermont', 51: 'Virginia', 53: 'Washington',
54: 'West Virginia', 55: 'Wisconsin', 56: 'Wyoming', 66: 'Guam',
72: 'Puerto Rico', 78: 'Virgin Islands'
}
# Sex of Respondent Mapping
sex_codes = {
1: 'Male',
2: 'Female'
}
# General Health Mapping
health_codes = {
1: 'Excellent',
2: 'Very Good',
3: 'Good',
4: 'Fair',
5: 'Poor',
7: 'Don’t know/Not Sure',
9: 'Refused'
}
# Function to map responses to 'Yes' and 'No/Unsure'
def map_yes_no_unsure(x):
    if pd.isna(x):
        return np.nan
    elif x == 1:
        return 'Yes'
    elif x in [2, 7, 9]:
        return 'No/Unsure'
    else:
        return 'No/Unsure' # Default to 'No/Unsure' for any unexpected values

# Map numeric codes to descriptive labels
df['state_name'] = df['_STATE'].map(state_codes)
df['sex'] = df['SEXVAR'].map(sex_codes)
df['genhlth_label'] = df['GENHLTH'].map(health_codes)
df['cvdcrhd4_label'] = df['CVDCRHD4'].apply(map_yes_no_unsure)
df['cvdstrk3_label'] = df['CVDSTRK3'].apply(map_yes_no_unsure)
df['chcocncr1_label'] = df['CHCOCNC1'].apply(map_yes_no_unsure)
df['havarth4_label'] = df['HAVARTH4'].apply(map_yes_no_unsure)

# Function to calculate weighted percentage
def weighted_percentage(data, var_label, weight='_LLCPWT'):
    grouped = data.groupby(['state_name', 'sex', var_label])[weight].sum()
    total = data.groupby(['state_name', 'sex'])[weight].sum()
    percentage = (grouped / total * 100).round(2)
    return percentage

# Calculate weighted percentages for each health indicator

# 1. Health Status
health_pct = weighted_percentage(
df[df['genhlth_label'].notna()],
'genhlth_label'
)

# 2. Heart Disease
heart_pct = weighted_percentage(
df[df['cvdcrhd4_label'].notna()],
'cvdcrhd4_label'
)

# 3. Stroke
stroke_pct = weighted_percentage(
df[df['cvdstrk3_label'].notna()],
'cvdstrk3_label'
)

# 4. Cancer
cancer_pct = weighted_percentage(
df[df['chcocncr1_label'].notna()],
'chcocncr1_label'
)

# 5. Arthritis
arthritis_pct = weighted_percentage(
df[df['havarth4_label'].notna()],
'havarth4_label'
)

# Function to print results in a structured format
def print_result(title, series, label_name):
    print(f"\n=== {title} ===")
    print(series.unstack(level=label_name).fillna('NaN'))

# Print the results
print_result("Health Status Distribution by State and Sex", health_pct, 'genhlth_label')
print_result("Heart Disease Distribution by State and Sex", heart_pct, 'cvdcrhd4_label')
print_result("Stroke Distribution by State and Sex", stroke_pct, 'cvdstrk3_label')
print_result("Cancer Distribution by State and Sex", cancer_pct, 'chcocncr1_label')
print_result("Arthritis Distribution by State and Sex", arthritis_pct, 'havarth4_label')

# Save the results to an Excel file with separate sheets for each indicator
with pd.ExcelWriter('health_statistics_by_state_and_sex.xlsx') as writer:
    health_pct.unstack('genhlth_label').to_excel(writer, sheet_name='Health Status')
    heart_pct.unstack('cvdcrhd4_label').to_excel(writer, sheet_name='Heart Disease')
    stroke_pct.unstack('cvdstrk3_label').to_excel(writer, sheet_name='Stroke')
    cancer_pct.unstack('chcocncr1_label').to_excel(writer, sheet_name='Cancer')
    arthritis_pct.unstack('havarth4_label').to_excel(writer, sheet_name='Arthritis')

print("\nResults have been successfully saved to 'health_statistics_by_state_and_sex.xlsx'.")