import numpy as np
import pandas as pd
import data_cleanup as data
import seaborn as sns
import matplotlib.pyplot as plt
from adjustText import adjust_text


people_data, promo_data, transaction_data, transfer_data = data.data_to_use()
pd.DataFrame.rename(people_data, columns={'Iphone': 'iPhone'}, inplace=True)

# Pie Chart for Devices (in percentage)
device_counts_df = people_data[['Android', 'iPhone', 'Desktop']].sum().reset_index()
device_counts_df.columns = ['Device', 'Count']
plt.figure(figsize=(6,6))
plt.pie(device_counts_df['Count'], labels=device_counts_df['Device'], autopct='%1.1f%%', startangle=90, counterclock=False)
plt.title('Device Count Distribution')
plt.savefig('figures/Device_Usage_Counts.png')  # Save figure

# Bar Plot for Country Distribution
country = people_data['country'].value_counts().reset_index()
country.columns = ['Country', 'Count']  # Rename columns
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='Country', y='Count', hue='Country', data=country)
plt.title('User Distribution by Country')
plt.xlabel('Country')
plt.ylabel('Count')
plt.savefig('figures/Country_Distribution.png')  # Save figure

# promo_data['responded'].replace({'Yes': 1, 'No': 0},inplace=True)
responses = promo_data['responded'].value_counts().reset_index()
responses.columns = ['Responses', 'Count']  # Rename columns
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='Responses', y='Count', hue='Responses', data=responses)
plt.title('Responses to Promotions')
plt.xlabel('Response ')
plt.ylabel('Total')
plt.savefig('figures/ResponsePlot.png')  # Save figure

transfer_years = transfer_data['year'].value_counts().reset_index()
transfer_years.columns = ['year', 'total']  # Rename columns
transfer_years = transfer_years.sort_values(by='year')

plt.figure(figsize=(12, 6))  # Create new figure
plt.plot(transfer_years['year'], transfer_years['total'], marker='o')
plt.title('Transfer Sales by Year')
plt.xlabel('Year')
plt.ylabel('Total Transfer Sales')
plt.savefig('figures/TransferSalesYearly.png')  # Save figure

sender_countries = transfer_data.merge(people_data[['id','country','city']], left_on='sender_id',right_on='id', how='inner')
sender_countries = sender_countries['country'].value_counts().reset_index()
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='country', y='count', hue='country', data=sender_countries)
plt.title('Transfer Sales by Country')
plt.xlabel('Country')
plt.ylabel('Total Transfer Sales')
plt.savefig('figures/TransferSalesCountry.png')  # Save figure

sender_cities = transfer_data.merge(people_data[['id','country','city']], left_on='sender_id',right_on='id', how='inner')
sender_cities = sender_cities['city'].value_counts().reset_index()
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='city', y='count', hue='city', data=sender_cities)
plt.title('Transfer Sales by City')
plt.xlabel('City')
plt.ylabel('Total Transfer Sales')
plt.savefig('figures/TransferSalesCity.png')  # Save figure

# print(promo_data.head())
# print(people_data.head())
# items = transaction_data['items'].reset_index()
# print(items)
# print(transfer_data.head())

# print(transaction_data['store'].value_counts()) #TODO: make barplot of this 

total_sales = {}
for item in transaction_data['items']:
    name = item[0]['name']
    total = int(item[0]['total'])
    if name in total_sales.keys():
        total_sales[name] += total
    else:
        total_sales[name] = 0
item_sales = pd.DataFrame(total_sales,index=['total']).T.reset_index().sort_values(by='total',ascending=False)
item_sales.columns = ['Item','Total Sales']

promo_p_item = promo_data['promotion'].value_counts().reset_index().sort_values(by='count',ascending=False)
promo_p_item.columns = ['Item','Total Promotions']


plt.figure(figsize=(12, 6))  # Create new figure

item_sales_promo = item_sales.merge(promo_p_item, on='Item', how='inner')

# Creating scatter plot
ax = sns.lmplot(x='Total Sales',
                y='Total Promotions',
                data=item_sales_promo,
                fit_reg=False, 
                aspect=2)

plt.title('Sales vs Promotions per Item')
plt.xlabel('Total Sales')
plt.ylabel('Total Promotions')

def label_point(x, y, val, ax):
    a = pd.DataFrame({'x': x, 'y': y, 'val': val})
    texts = []
    
    for _, point in a.iterrows():
        texts.append(plt.text(point['x'] + np.random.uniform(-1.2, 1.2),
                              point['y'] + np.random.uniform(-1.2, 1.2),
                              str(point['val'])))
    
    # Adjust labels to prevent overlapping
    adjust_text(texts, ax=plt.gca(), expand_points=(1.2, 1.5))

label_point(item_sales_promo['Total Sales'], item_sales_promo['Total Promotions'], item_sales_promo['Item'], plt.gca())
plt.show()
