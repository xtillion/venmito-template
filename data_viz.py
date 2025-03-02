import numpy as np
import pandas as pd
import data_cleanup as data
import seaborn as sns
import matplotlib.pyplot as plt
from adjustText import adjust_text
import helpers.cleanup_funcs as cleanup

people_data, promo_data, transaction_data, transfer_data = data.data_to_use()
pd.DataFrame.rename(people_data, columns={'Iphone': 'iPhone'}, inplace=True)

# CREATING VISUALIZATION FOR DEVICE PERCENTAGE FOR USERS 
device_counts_df = people_data[['Android', 'iPhone', 'Desktop']].sum().reset_index()
device_counts_df.columns = ['Device', 'Count']
plt.figure(figsize=(6,6))
plt.pie(device_counts_df['Count'], labels=device_counts_df['Device'], autopct='%1.1f%%', startangle=90, counterclock=False)
plt.title('Device Count Distribution')
plt.savefig('figures/Device_Usage_Counts.png')  # Save figure

### CREATING VISUALIZATION FOR USER DISTRIBUTION BY COUNTRY
country = people_data['country'].value_counts().reset_index()
country.columns = ['Country', 'Count']  # Rename columns
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='Country', y='Count', hue='Country', data=country)
plt.title('User Distribution by Country')
plt.xlabel('Country')
plt.ylabel('Count')
plt.savefig('figures/Country_Distribution.png')  # Save figure

### CREATING VISUALIZATION FOR RESPONSES TO PROMOTIONS
responses = promo_data['responded'].value_counts().reset_index()
responses.columns = ['Responses', 'Count']  # Rename columns
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='Responses', y='Count', hue='Responses', data=responses)
plt.title('Responses to Promotions')
plt.xlabel('Response ')
plt.ylabel('Total')
plt.savefig('figures/ResponsePlot.png')  # Save figure


### CREATING VISUALIZATION FOR TRANSFER SALES BY YEAR
transfer_years = transfer_data['year'].value_counts().reset_index()
transfer_years.columns = ['year', 'total']  # Rename columns
transfer_years = transfer_years.sort_values(by='year')
plt.figure(figsize=(12, 6))  # Create new figure
plt.plot(transfer_years['year'], transfer_years['total'], marker='o')
plt.title('Transfer Sales by Year')
plt.xlabel('Year')
plt.ylabel('Total Transfer Sales')
plt.savefig('figures/TransferSalesYearly.png')  # Save figure

### CREATING VISUALIZATION FOR TRANSFER SALES BY COUNTRY
sender_countries = transfer_data.merge(people_data[['id','country','city']], left_on='sender_id',right_on='id', how='inner')
sender_countries = sender_countries['country'].value_counts().reset_index()
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='country', y='count', hue='country', data=sender_countries)
plt.title('Transfer Sales by Country')
plt.xlabel('Country')
plt.ylabel('Total Transfer Sales')
plt.savefig('figures/TransferSalesCountry.png')  # Save figure


### CREATING VISUALIZATION FOR WHERE PEOPLE ARE SENDING MONEY FROM
sender_cities = transfer_data.merge(people_data[['id','country','city']], left_on='sender_id',right_on='id', how='inner')
sender_cities = sender_cities['city'].value_counts().reset_index()
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='city', y='count', hue='city', data=sender_cities)
plt.title('Transfer Sales by City')
plt.xlabel('City')
plt.ylabel('Total Transfer Sales')
plt.savefig('figures/TransferSalesCity.png')  # Save figure

sender_cities = transfer_data.merge(people_data[['id','country','city']], left_on='sender_id',right_on='id', how='inner')
sender_cities = sender_cities['city'].value_counts().reset_index()

## CREATING VISUAL FOR TRANSACTIONS PER STORE
transactions_per_store = transaction_data['store'].value_counts().reset_index()
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='store', y='count', hue='store', data=transactions_per_store)
plt.title('Transactions per Store')
plt.xlabel('Store')
plt.ylabel('Total Transactions')
plt.savefig('figures/TransactionsPerStore.png')  # Save figure


### CREATING VISUALIZATION FOR TOTAL SALES VS PROMOTIONS PER ITEM
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
plt.figure(figsize=(12, 6))  
item_sales_promo = item_sales.merge(promo_p_item, on='Item', how='inner')
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