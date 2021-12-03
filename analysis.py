import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import scipy.stats as st
from scipy.stats import pearsonr


conn = create_engine('sqlite:///TaoProject.db').connect()
data_sql = pd.read_sql_table('historical_quaterly_GDP',conn)
#print('The GDP of the US:')
quarter = []
a = data_sql['quater']
for i in a:
    quarter.append(i)
#print(quarter)
GDP = []
b = data_sql['GDP']
for i in b:
    GDP.append(i)
#print(GDP)
fig = plt.figure(figsize=(28,10))
plt.xlabel("Quarter,Year")
plt.ylabel("GDP")
plt.title("GDP From Q3 2019")
plt.plot(quarter,GDP,label = 'GDP')
plt.legend()
plt.savefig('quarterly_GDP_graph.jpg')
plt.show()

conn = create_engine('sqlite:///TaoProject.db').connect()
data_sql = pd.read_sql_table('historical_gold_price',conn)
#print('Gold price:')
gold_prices = []
a = data_sql['price']
for i in a:
    gold_prices.append(i)
#print(gold_prices)
date = []
b = data_sql['date']
for i in b:
    i = str(i)
    i = i[0:10]
    date.append(i)
#print(date)
fig= plt.figure(figsize=(28,10))
plt.xlabel("Month,Year")
plt.ylabel("gold prices")
plt.title("Gold Prices From Sep 2019")
plt.plot(date,gold_prices,label = 'gold price',color = 'r')
plt.legend()
plt.savefig('gold_prices.jpg')
plt.show()

conn = create_engine('sqlite:///TaoProject.db').connect()
data_sql = pd.read_sql_table('historical_crude_oil_price',conn)
#print('Gold price:')
oil_prices = []
a = data_sql['price']
for i in a:
    oil_prices.append(i)
#print(oil_prices)
fig= plt.figure(figsize=(28,10))
plt.xlabel("Month,Year")
plt.ylabel("Crude oil prices")
plt.title("Crude Oil Prices From Sep 2019")
plt.plot(date,oil_prices,label = 'Crude oil price',color = 'g')
plt.legend()
plt.savefig('oil_prices.jpg')
plt.show()

pccs_gold_and_oil = pearsonr(gold_prices, oil_prices)
print('Pearson Correlation Coefficient of Gold Prices and Oil Prices is:')
print(pccs_gold_and_oil[0])
print('='*50)

quarterly_ave_gold_prices = []
quarterly_ave_gold_prices.append(gold_prices[0])
for i in range(1,22,3):
    ave = sum(gold_prices[i:i+3])/3
    quarterly_ave_gold_prices.append(ave)
ave_last_two = sum(gold_prices[-2:])/2
quarterly_ave_gold_prices.append(ave_last_two)
#print(quarterly_ave_gold_prices)
#print(len(quarterly_ave_gold_prices))
fig= plt.figure(figsize=(24,7))
plt.xlabel("Quarter,Year")
plt.ylabel("quarterly average gold prices")
plt.title(" quarterly average gold prices From Q3 2019")
plt.plot(quarter,quarterly_ave_gold_prices,label = 'quarterly average oil prices',color = 'c')
plt.legend()
plt.savefig('quarterly_ave_gold_prices.jpg')
plt.show()

pccs_GDP_and_gold = pearsonr(quarterly_ave_gold_prices, GDP)
print('Pearson Correlation Coefficient of Gold Prices and GDP is:')
print(pccs_GDP_and_gold[0])
print('='*50)

quarterly_ave_oil_prices = []
quarterly_ave_oil_prices.append(oil_prices[0])
for i in range(1,22,3):
    ave = sum(oil_prices[i:i+3])/3
    quarterly_ave_oil_prices.append(ave)
ave_last_two = sum(oil_prices[-2:])/2
quarterly_ave_oil_prices.append(ave_last_two)
#print(quarterly_ave_oil_prices)
#print(len(quarterly_ave_oil_prices))
fig= plt.figure(figsize=(24,7))
plt.xlabel("Quarter,Year")
plt.ylabel("quarterly average oil prices")
plt.title(" quarterly average oil prices From Q3 2019")
plt.plot(quarter,quarterly_ave_oil_prices,label = 'quarterly average oil prices',color = 'c')
plt.legend()
plt.savefig('quaterly_ave_oil_prices.jpg')
plt.show()

pccs_GDP_and_oil = pearsonr(quarterly_ave_oil_prices, GDP)
print('Pearson Correlation Coefficient of Gold Prices and GDP is:')
print(pccs_GDP_and_oil[0])
print('='*50)

#linear regression:
slope, intercept, r_value, p_value, std_err = st.linregress(quarterly_ave_oil_prices,GDP)
"""def oil_to_GDP(parameter,x):
    if parameter.lower == 'oil':
        predict_GDP = slope*x + intercept
        print('the GDP will be：',predict_GDP)
    elif parameter.lower == 'gdp':
        x = float(x)
        predict_oil = (x-intercept)/slope
        print('the oil price will be:', predict_oil)
    else:
        print('Please enter:\'the original object\',\'the original value\'.'
              ' For example: GDP,19238.63')"""
slope = str(slope)
intercept = str(intercept)
print('Linear function between oil prices and GDP of the US:')
print('GDP='+slope+'*oil prices+'+intercept)
print('='*50)

#User interact
user_input = input('Do you want to predict GDP or Oil price (by inputting Oil price or GDP respectively[y/n]?')
while True:
    if user_input == 'y':
        parameter = input('Do you want to convert \'GDP\' or \'Oil\'?: ')
        if parameter.lower() == 'oil':
            x = input('Please enter the value: ')
            x = float(x)
            slope = float(slope)
            intercept = float(intercept)
            predict_GDP = slope * x + intercept
            print('the GDP will be：', predict_GDP)
        elif parameter.lower() == 'gdp':
            x = input('Please enter the value: ')
            x = float(x)
            slope = float(slope)
            intercept = float(intercept)
            predict_oil = (x - intercept) / slope
            print('the oil price will be:', predict_oil)
        else:
            print('Please enter:\'the original object\',\'the original value\'.'
                  ' For example: GDP,19238.63')
        user_input = input('Do you want to try again[y/n]?')
    elif user_input == 'n':
        break
    else:
        print("Please Enter \'y\' or \'n\'")
        user_input = input('Do you want to predict GDP or Oil price (by inputting Oil price or GDP respectively[y/n]?')

print('Thank you for checking my project. Have a nice holiday.  :)')
