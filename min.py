import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_excel("GooglePlaystore.xlsx")

# Remove invalid records
data = data[data['Reviews'] != '3.0M']
data = data[~data.apply(lambda x: x.astype(str).str.contains('Varies with device')).any(axis=1)]

# Process Android version and Installs
data['Android Ver'] = data['Android Ver'].str.extract(r'(\d+\.\d+)')
data['Installs'] = data['Installs'].str.replace('[+,]', '', regex=True).astype(int)

# Convert 'Reviews' to integer for processing
data['Reviews'] = data['Reviews'].astype(int)

# Handle missing ratings
def fill_missing_ratings(row):
    if pd.isna(row['Rating']):
        if row['Reviews'] < 100 and row['Installs'] < 50000:
            return None
        else:
            return category_averages[row['Category']]
    return row['Rating']

# Calculate average ratings per category rounded to two decimal places
category_averages = data.groupby('Category')['Rating'].mean().round(2)

# Apply the function and drop rows where rating is set to None
data['Rating'] = data.apply(fill_missing_ratings, axis=1)
data = data.dropna(subset=['Rating'])

# Convert 'Size' to integer bytes
def convert_size(size):
    if 'M' in size:
        return int(float(size.replace('M', '')) * 1000000)
    elif 'k' in size or 'K' in size:
        return int(float(size.replace('k', '').replace('K', '')) * 1000)
    else:
        return None  # Assume other formats are already removed

data['Size'] = data['Size'].apply(convert_size)
data = data.dropna(subset=['Size'])

# Optionally, save the cleaned data
data.to_excel("Cleaned_GooglePlaystore.xlsx", index=False)

import pandas as pd

#Load data
data = pd.read_excel("GooglePlaystore.xlsx")

#Remove invalid records
data = data[data['Reviews'] != '3.0M']
data = data[~data.apply(lambda x: x.astype(str).str.contains('Varies with device')).any(axis=1)]

#Process Android version and Installs
data['Android Ver'] = data['Android Ver'].str.extract(r'(\d+\.\d+)')
data['Installs'] = data['Installs'].str.replace('[+,]', '', regex=True).astype(int)

#Convert 'Reviews' to integer for processing
data['Reviews'] = data['Reviews'].astype(int)

def fill_missing_ratings(row):
    if pd.isna(row['Rating']):
        if row['Reviews'] < 100 and row['Installs'] < 50000:
            return None
        else:
            return category_averages[row['Category']]
    return row['Rating']

#Calculate average ratings per category rounded to two decimal places
category_averages = data.groupby('Category')['Rating'].mean().round(2)

data['Rating'] = data.apply(fill_missing_ratings, axis=1)
data = data.dropna(subset=['Rating'])

#Convert 'Size' to integer
def convert_size(size):
    if 'M' in size:
        return int(float(size.replace('M', '')) * 1000000)
    elif 'k' in size or 'K' in size:
        return int(float(size.replace('k', '').replace('K', '')) * 1000)
    else:
        return None  

data['Size'] = data['Size'].apply(convert_size)
data = data.dropna(subset=['Size'])

data.to_excel("Cleaned_GooglePlaystore.xlsx", index=False, engine='openpyxl')

def stats():
    x = categoryRatingStats = data.groupby('Category')['Rating'].describe()
    print(x)
    
stats()

#iso free apps
freeApps = data[data['Type'] == 'Free']

#get top 3 apps of a column
def getTop3HelperFunc(group, column_name):
    return group.nlargest(3, column_name)[['Category', 'App', column_name]]

#get top 3 apps using the previous function to actually get the thang
def top3Apps(dataframe, column_name):
    topApps = dataframe.groupby('Category').apply(getTop3HelperFunc, column_name=column_name)
    topApps.reset_index(drop=True, inplace=True)
    return topApps

topRatedApps = top3Apps(freeApps, 'Rating')
topInstalledApps = top3Apps(freeApps, 'Installs')
topReviewedApps = top3Apps(freeApps, 'Reviews')

print(f"Top Rated Free Apps: {topRatedApps.head()}")
print(f"\nTop Installed Free Apps: {topInstalledApps.head()}")
print(f"\nTop Reviewed Free Apps: {topReviewedApps.head()}")

paidApps = data[data['Type'] == 'Paid']
averagePrice = paidApps['Price'].mean()
maxPrice = paidApps['Price'].max()
minPrice = paidApps['Price'].min()
print(f"Average Price of Paid Apps: ${averagePrice:.2f}")
print(f"Maximum Price of Paid Apps: ${maxPrice:.2f}")
print(f"Minimum Price of Paid Apps: ${minPrice:.2f}")



#Assume data is loaded and preprocessed
data = pd.read_excel("Cleaned_GooglePlaystore.xlsx")  # Load the cleaned data

#Split 'Genres' into lists and explode
data['Genres'] = data['Genres'].str.split('; ')
exploded_genres = data.explode('Genres')

#Count applications per genre
genre_counts = exploded_genres['Genres'].value_counts()

#Pie chart of applications per genre
plt.figure(figsize=(10, 8))
genre_counts.plot.pie(autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Applications Per Genre')
plt.ylabel('')  # Remove the y-label as it's unnecessary
plt.show()

#3-2
data = df[df['Category'].isin(['BUSINESS', 'EDUCATION'])]
plt.figure(figsize=(8, 6))
boxplot = data.boxplot(by='Category', column='Rating', grid=False)

plt.title('Box Plot of Ratings for Business and Education Categories')
plt.suptitle('') 
plt.ylabel('Rating')
plt.xlabel('Category')
plt.show()
