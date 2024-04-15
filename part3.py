import pandas as pd

# Load the DataFrame
dataframe1 = pd.read_excel('GooglePlaystore.xlsx')

# Check column names if unsure where the value might be
print(dataframe1.columns)

# Assuming the name is in a column named 'App'
dataframe1 = dataframe1[dataframe1['App'] != "InterracialCupid - Interracial Dating App"]

# Print the DataFrame to see the result
print(dataframe1)
