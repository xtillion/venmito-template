import numpy as np
import pandas as pd
import data_cleanup as data
import seaborn as sns
import matplotlib.pyplot as plt

people_data, promo_data, transaction_data, transfer_data = data.data_to_use()
pd.DataFrame.rename(people_data, columns={'Iphone': 'iPhone'}, inplace=True)

# Creating a DataFrame for plotting
device_counts_df = people_data[['Android', 'iPhone', 'Desktop']].sum().reset_index()
device_counts_df.columns = ['Device', 'Count']
plt.figure(figsize=(10, 6))
sns.barplot(x='Device', y='Count', hue='Device', data=device_counts_df)
plt.title('Device Usage Counts')
plt.xlabel('Device')
plt.ylabel('Count')
plt.savefig('figures/Device_Usage_Counts.png')  # Save figure
# plt.show()  # Display plot


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
sns.barplot(x='Responses', y='Total', hue='Responses', data=responses)
plt.title('Responses to Promotions')
plt.xlabel('Response ')
plt.ylabel('Total')
plt.savefig('figures/ResponsePlot.png')  # Save figure
plt.show()  # Display plot
