import numpy as np
import pandas as pd
import data_cleanup as data
import seaborn as sns
import matplotlib.pyplot as plt

people_data, promo_data, transaction_data, transfer_data = data.data_to_use()
pd.DataFrame.rename(people_data, columns={'Iphone': 'iPhone'}, inplace=True)

#Creating count for Devices
device_counts = people_data[['Android', 'iPhone', 'Desktop']].sum()
# Creating a DataFrame for plotting
device_counts_df = device_counts.reset_index()
device_counts_df.columns = ['Device', 'Count']
plt.figure(figsize=(10, 6))
sns.barplot(x='Device', y='Count', data=device_counts_df, palette='viridis')
plt.title('Device Usage Counts')
plt.xlabel('Device')
plt.ylabel('Count')
plt.savefig('figures/Device Usage Counts.png')
