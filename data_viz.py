import numpy as np
import pandas as pd
import data_cleanup as data
import seaborn as sns
import matplotlib.pyplot as plt

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
# plt.show()  # Display plot

# promo_data['responded'].replace({'Yes': 1, 'No': 0},inplace=True)
responses = promo_data['responded'].value_counts().reset_index()
responses.columns = ['Responses', 'Count']  # Rename columns
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='Responses', y='Count', hue='Responses', data=responses)
plt.title('Responses to Promotions')
plt.xlabel('Response ')
plt.ylabel('Total')
plt.savefig('figures/ResponsePlot.png')  # Save figure
# plt.show()  # Display plot

transfer_years = transfer_data['year'].value_counts().reset_index()
transfer_years.columns = ['year', 'total']  # Rename columns
transfer_years = transfer_years.sort_values(by='year')

plt.figure(figsize=(12, 6))  # Create new figure
plt.plot(transfer_years['year'], transfer_years['total'], marker='o')
plt.title('Transfer Sales by Year')
plt.xlabel('Year')
plt.ylabel('Total Transfer Sales')
plt.savefig('figures/TransferSales.png')  # Save figure
# plt.show()

sender_countries = transfer_data.merge(people_data[['id','country','city']], left_on='sender_id',right_on='id', how='inner')
sender_countries = sender_countries['country'].value_counts().reset_index()
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='country', y='count', hue='country', data=sender_countries)
plt.show()

# print(promo_data.head())
# print(people_data.head())
# print(transaction_data.head())
# print(transfer_data.head())