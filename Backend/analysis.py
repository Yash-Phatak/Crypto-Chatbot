import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import datetime
warnings.filterwarnings('ignore')

data = pd.read_csv('combined_data.csv')
data = data.drop(['SNo'],axis=1) #Dropping SNO column
data['Date']= data['Date'].str.split().str.get(0) #Separating the date
data['Date'] = pd.to_datetime(data['Date']) #Converting Date String to Date timestamp

cryptocurrencies = []
cryptocurrencies.extend(i.lower() for i in data['Name'] if i.lower() not in cryptocurrencies)

#Plotting
def highplot(name):
    selected_data = data[data['Name'].str.lower()==name.lower()]
    plt.figure(figsize=(10,6))
    plt.plot(selected_data['Date'],selected_data['High'])
    plt.title(f"{name.capitalize()} Highs over Time")
    plt.xlabel('Date')
    plt.ylabel('High')
    plt.xticks(rotation=45)
    plt.grid(False)
    plt.tight_layout()
    return plt

#Comparison 
def compareit(name1,name2):
    cryp1 = data[data['Name']==name1]
    cryp2 = data[data['Name']==name2]
    plt.figure(figsize=(10,6))
    plt.plot(cryp1['Date'],cryp1['Close'],label=name1)
    plt.plot(cryp2['Date'],cryp2['Close'],label=name2)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title(f'Comparison of {name1} and {name2} Closing Prices')
    plt.legend()
    plt.xticks(rotation=45)
    plt.yscale('log')
    plt.tight_layout()
    print(1)
    return plt

crypto_name1 = 'Bitcoin'
crypto_name2 = 'Ethereum'
plot = compareit(crypto_name1, crypto_name2)


