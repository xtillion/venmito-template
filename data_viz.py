import numpy as np
import pandas as pd
import data_cleanup as data
import seaborn as sns
import matplotlib.pyplot as plt
from adjustText import adjust_text
import helpers.cleanup_funcs as cleanup
import helpers.data_viz_funcs as viz_help


people_data, promo_data, transaction_data, transfer_data = data.data_to_use()
pd.DataFrame.rename(people_data, columns={'Iphone': 'iPhone'}, inplace=True)

# CREATING VISUALIZATION FOR DEVICE PERCENTAGE FOR USERS 
device_counts_df = people_data[['Android', 'iPhone', 'Desktop']].sum().reset_index()
device_counts_df.columns = ['Device', 'Count']
plt.figure(figsize=(6,6))
plt.pie(device_counts_df['Count'], labels=device_counts_df['Device'], autopct='%1.1f%%', startangle=90, counterclock=False)
plt.title('User Device Distribution')
plt.savefig('figures/Device_Usage_Counts.png')  # Save figure

### CREATING VISUALIZATION FOR USER DISTRIBUTION BY COUNTRY
country = people_data['country'].value_counts().reset_index()
country.columns = ['Country', 'Count']
country = country.sort_values(by='Count', ascending=False) 
sns.set_theme(style='whitegrid')  
plt.figure(figsize=(14, 7))
ax = sns.barplot(x='Country', y='Count', data=country, hue= 'Country', palette='viridis',legend=False)
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=10, color='black')
plt.title('User Distribution by Country', fontsize=14, weight='bold')
plt.xlabel('Country')
plt.ylabel('Total Users')
plt.xticks(rotation=45)  
# Grid and layout
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout() 
plt.savefig('figures/Country_Distribution.png', dpi=300)

### CREATING VISUALIZATION FOR USER DISTRIBUTION BY City
city = people_data['city'].value_counts().reset_index()
city.columns = ['City', 'Count']
city = city.sort_values(by='Count', ascending=False) 
plt.figure(figsize=(20,10))
ax = plt.subplot(111, polar=True)
plt.axis('off')
upperLimit = 100
lowerLimit = 30
max_value = city['Count'].max()
slope = (max_value - lowerLimit) / max_value
heights = slope * city['Count'] + lowerLimit
width = 2 * np.pi / len(city.index)
indexes = list(range(1, len(city.index) + 1))
angles = [element * width for element in indexes]
bars = ax.bar(x=angles, height=heights, width=width, bottom=lowerLimit, linewidth=2, edgecolor="white", color=plt.cm.tab20.colors)
labelPadding = 4
for bar, angle, height, label in zip(bars, angles, heights, city["City"]):
    rotation = np.rad2deg(angle)
    alignment = "right" if angle >= np.pi / 2 and angle < 3 * np.pi / 2 else "left"
    if alignment == "right":
        rotation = rotation + 180
    ax.text(x=angle, 
            y=lowerLimit + bar.get_height() + labelPadding, 
            s=label, 
            ha=alignment, 
            va='center', 
            rotation=rotation, 
            rotation_mode="anchor")
plt.savefig('figures/City_Distribution.png')

### CREATING VISUALIZATION FOR RESPONSES TO PROMOTIONS
responses = promo_data['responded'].value_counts().reset_index()
responses.columns = ['Responses', 'Count']  # Rename columns
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='Responses', y='Count', hue='Responses', data=responses)
plt.title('Responses to Promotions')
plt.xlabel('Response')
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
plt.ylabel('Total Amount of Transfers')
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
plt.title('Sales vs Promotions per Item', pad=-5)
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
plt.savefig('figures/SalesPromoItem.png')
###CREATING VISUALIZATION FOR TRANSFER INTERNATIONAL VS DOMESTIC
send_id_location = transfer_data.merge(people_data[['id','country','city']], left_on='sender_id',right_on='id', how='inner')
send_id_location.rename(columns={'country':'sender_country','city':'sender_city'},inplace=True)
send_id_location = send_id_location.merge(people_data[['id','country','city']], left_on='recipient_id',right_on='id', how='inner')
send_id_location.rename(columns={'country':'reciepient_country','city':'recipient_city'},inplace=True)
send_id_location['international'] = send_id_location.apply(lambda x: viz_help.check_if_international(x),axis = 1)
transfer_international = send_id_location['international'].value_counts()
plt.figure(figsize=(6, 6))
transfer_international.plot.pie(autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'], labels=['Domestic', 'International'])
plt.title('Distribution of International vs. Domestic Transfers')
plt.ylabel('') 
plt.savefig('figures/DistribInternationalDomestic.png')
# send_recieve = transfer_data.merge(people_data[['id','country','city']], left_on='recipient_id',right_on='id', how='inner')
# send_recieve = send_recieve['city'].value_counts().reset_index()


###Checking if person buys what they're getting promotions on
person_promo = promo_data[['phone','promotion','responded']]
person_promo = person_promo.merge(transaction_data,on='phone',how='inner')
person_promo['promo_bought'] = person_promo.apply(lambda x: viz_help.check_if_bought(x),axis = 1)
promo_bought= person_promo['promo_bought'].value_counts().reset_index()
plt.figure(figsize=(12, 6))  # Create new figure
sns.barplot(x='promo_bought', y='count', hue='promo_bought', data=promo_bought)
plt.title('Promotions vs Actual Purchase')
plt.xlabel('Bought What Was Promoted')
plt.ylabel('Count')
plt.savefig('figures/PromotionBought.png')  # Save figure


