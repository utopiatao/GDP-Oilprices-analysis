import sqlite3
import datetime
from bs4 import BeautifulSoup
import requests
import webbrowser as wbb
import urllib.request, urllib.parse, urllib.error
import xlrd
import pandas as pd
import http.client
from sqlalchemy import create_engine

has_csv = input('Did you manually download \'F005006__3m.csv\'?[y/n]')
### Download CSV file of Historical Crude Oil Prices
while True:
    if has_csv == 'n':
        content = requests.get('https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=f005006__3&f=m')
        soup = BeautifulSoup(content.content, 'html.parser')
        tags = soup('a')
        tag1 = ""
        for tag in tags:
            tag = tag.get('href',None)
            tag = str(tag)
            if ".xls" in tag:
                tag1 = str(tag)
        index = tag1.find("/hist")
        index2 = tag1.find("xls/")
        tag2 = tag1[index:]
        historic_oil_price_csv_name = tag1[(index2+4):]
        historic_crud_oil = "https://www.eia.gov/dnav/pet" + tag2
        historic_crud_oil_csv = wbb.open (historic_crud_oil)
        print('Creating the Database.....')
        break
    elif has_csv == 'y':
        break
    else:
        print('Please enter \'y\' for yes, \'n\' for no:')
        has_csv = input('Did you manually download \'F005006__3m.csv\'?[y/n]')

###if you have the csv files, you may skip the code above
print('Creating the Database.....')
content = requests.get('https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=f005006__3&f=m')
soup = BeautifulSoup(content.content, 'html.parser')
tags = soup('a')
tag1 = ""
for tag in tags:
    tag = tag.get('href',None)
    tag = str(tag)
    if ".xls" in tag:
        tag1 = str(tag)
index = tag1.find("/hist")
index2 = tag1.find("xls/")
tag2 = tag1[index:]
historic_oil_price_csv_name = tag1[(index2+4):]
historic_crud_oil = "https://www.eia.gov/dnav/pet" + tag2
data = xlrd.open_workbook(historic_oil_price_csv_name)
table = data.sheet_by_name(u'Data 1')
oil_price_dictionary = {}
lst = []
oilprices = []
for line in table:
    lst.append(line)
#print(lst)
del lst[0:3]
for i in lst:
    date = str(i[0])
    date = float(date[7:])
    price = str(i[1])
    price = float(price[7:])
    if date > 43722:
        oilprices.append(price)
month_year = "09-01-2019"
the_months = []
for i in range(0,len(oilprices)):
    empty_lst = []
    empty_lst.append(oilprices[i])
    monthyear = month_year.split('-')
    month = int(monthyear[0])
    year = int(monthyear[2])
    day = int(monthyear[1])
    month_year = datetime.date(year,month,day)
    the_months.append(month_year)
    oil_price_dictionary[month_year] = empty_lst[0]
    if month != 12:
        month +=1
    else:
        year += 1
        month = 1
    month = str(month)
    year = str(year)
    day = str(day)
    month_year = month + '-' + day + '-' + year
#print(oil_price_dictionary)
###write oil prices into a table of a db file
conn = sqlite3.connect('TaoProject.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = conn.cursor()
not_important = 0
try:
    cur.execute('CREATE TABLE historical_crude_oil_price (date DATE, price real)')
except:
    not_important = 1
for keys,values in oil_price_dictionary.items():
    my_list = list()
    datevalue = str(keys)
    my_list.append(datevalue)
    pricevalue = float(values)
    my_list.append(pricevalue)
    my_list = tuple(my_list)
    my_list = str(my_list)
    cur.execute('INSERT INTO historical_crude_oil_price VALUES' + my_list)
conn.commit()
conn.close()

### Get historical quaterly GDP
quarterly_GDP = []
urlpages = ["https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=2019-07-01#",
            'https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=2019-10-01#',
            "https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=2020-01-01#",
            "https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=2020-04-01#",
            "https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=2020-07-01#",
            "https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=2020-10-01#",
            "https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=2021-01-01#",
            "https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=2021-04-01#",
            "https://fred.stlouisfed.org/release/tables?rid=53&eid=13026&od=#"]
for i in urlpages:
    page = urllib.request.urlopen(i)
    soup = BeautifulSoup(page,'html.parser')
    #print(soup)
    table = soup.find('td',attrs = {'class':'fred-rls-elm-vl-td'})
    #print(table)
    value = table.get_text().strip().replace(',',"")
    value = float(value)
    quarterly_GDP.append(value)
#print(quarterly_GDP)
GDP_growth = []
for i in range(0,8):
    growth = int(quarterly_GDP[i]-quarterly_GDP[i+1])
    GDP_growth.append(growth)
#print(GDP_growth)
GDP_growth_dictionary = {}
quater = 'Q3,2019'
for i in range(0,len(quarterly_GDP)):
    GDP_growth_dictionary[quater] = quarterly_GDP[i]
    if quater[1] != '4':
        old_string = quater[1]
        season = int(float(quater[1])) + 1
        season = str(season)
        quater = quater.replace(old_string, season,1)
    else:
        GDP_year = int(float(quater[3:7]))
        GDP_year = str(GDP_year+1)
        quater = 'Q1,'+GDP_year
#print(GDP_growth_dictionary)

###write GDP into a table of a db file
conn = sqlite3.connect('TaoProject.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = conn.cursor()
not_important = 0
try:
    cur.execute('CREATE TABLE historical_quaterly_GDP (quater TEXT , GDP REAL)')
except:
    not_important = 1
for keys, values in GDP_growth_dictionary.items():
    my_list = list()
    datevalue = str(keys)
    my_list.append(datevalue)
    pricevalue = float(values)
    my_list.append(pricevalue)
    my_list = tuple(my_list)
    my_list = str(my_list)
    cur.execute('INSERT INTO historical_quaterly_GDP VALUES' + my_list)
conn.commit()
conn.close()

### Use API get historical gold prices
conn = http.client.HTTPSConnection("www.goldapi.io")
payload = ''
headers = {
  'x-access-token': 'goldapi-4490ztkwbniq43-io',
  'Content-Type': 'application/json'
}
goldprices = []
first_month = '20190925'
for i in oilprices:
    conn.request("GET", "/api/XAU/USD/"+first_month, payload, headers)
    res = conn.getresponse()
    data = res.read()
    a = data.decode('utf-8')
    index = a.find("price\":")
    int(index)
    goldprice = float(a[index+7:index+11])
    goldprices.append(goldprice)
    if first_month[4:6] == '12':
        first_month = int(first_month)
        first_month += 8900
        first_month = str(first_month)
    else:
        first_month = int(first_month) + 100
        first_month = str(first_month)
#print(goldprices)


###write GDP into a table of a db file
conn = sqlite3.connect('TaoProject.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = conn.cursor()
not_important = 0
try:
    cur.execute('CREATE TABLE historical_gold_price (date DATE, price real)')
except:
    not_important = 1
for i in range(0, len(goldprices)):
    my_list = list()
    datevalue = str(the_months[i])
    my_list.append(datevalue)
    pricevalue = float(goldprices[i])
    my_list.append(pricevalue)
    my_list = tuple(my_list)
    my_list = str(my_list)
    cur.execute('INSERT INTO historical_gold_price VALUES' + my_list)
conn.commit()
conn.close()
print('Database has been created successfully!')
"""
### print first 5 rows of the data
conn = create_engine('sqlite:///TaoProject.db').connect()
data_sql = pd.read_sql_table('historical_quaterly_GDP',conn)
print('The GDP of the US:')
print(data_sql.head())
print('='*50)
conn = create_engine('sqlite:///TaoProject.db').connect()
data_sql = pd.read_sql_table('historical_crude_oil_price',conn)
print('Historical crude oil prices:')
print(data_sql.head())
print('='*50)
conn = create_engine('sqlite:///TaoProject.db').connect()
data_sql = pd.read_sql_table('historical_gold_price',conn)
print('Historical gold prices:')
print(data_sql.head())
"""
