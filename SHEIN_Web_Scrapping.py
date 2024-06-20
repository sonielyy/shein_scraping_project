#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import Libraries
from selenium import webdriver
from time import sleep
import pandas as pd

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure Web Driver for Web Scraping
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Enter Web Site
driver.get('https://us.shein.com/recommend/Women-New-in-sc-100161222.html?adp=35242185&categoryJump=true&ici=us_tab03navbar03menu01dir02&src_identifier=fc%3DWomen%20Clothing%60sc%3DWomen%20Clothing%60tc%3DShop%20by%20category%60oc%3DNew%20in%60ps%3Dtab03navbar03menu01dir02%60jc%3DitemPicking_100161222&src_module=topcat&src_tab_page_id=page_home1718006855109')

# Sleep Determined for Captcha
sleep(4)
driver.maximize_window()
sleep(4)

# Close the Pop-up
button = driver.find_element(By.CLASS_NAME, 'sui-icon-common__wrap.she-close.homepage-she-close')
button.click()
sleep(4)

# Close the Second Pop-up
button = driver.find_element(By.CSS_SELECTOR, 'i.svgicon.svgicon-arrow-left')
button.click()
sleep(4)

# Item Elements
name_elements = driver.find_elements(By.CLASS_NAME, 'product-card__goods-title-container')
sleep(2)
    
# Price Elements
price_elements = driver.find_elements(By.CLASS_NAME, 'product-card__prices-info')
sleep(2)

# Rating Elements
rating_elements = driver.find_elements(By.CLASS_NAME, 'start-text')
sleep(1)

# Rating_2 Elements -- Extra lists created because of dynamic texts
rating2_elements = driver.find_elements(By.CLASS_NAME, 'start-text')
sleep(1)

# Rating_3 Elements
rating3_elements = driver.find_elements(By.CLASS_NAME, 'start-text')
sleep(2)

# Items will store in Lists
item_list = []
price_list = []
rating_list = []
rating2_list = []
rating3_list = []

# Add elements to Lists
for name in name_elements:
    item_list.append(name.text)
for price in price_elements:
    price_list.append(price.text)
for rating in rating_elements:
    rating_list.append(rating.text)
for rating2 in rating2_elements:
    rating2_list.append(rating2.text)
for rating3 in rating3_elements:
    rating3_list.append(rating3.text)


driver.close()


# In[133]:


# Check the Rating List for Anomaly
print(rating_list)
print(rating2_list)
print(rating3_list)


# In[134]:


# If one of the rating lists containts the missing element, overwrite it
for i in range(len(rating_list)):
    if rating_list[i] == '':
        rating_list[i] = rating2_list[i]
for i in range(len(rating_list)):
    if rating_list[i] == '':
        rating_list[i] = rating3_list[i]


# In[135]:


# Create the Data Frame
df1 = pd.DataFrame(zip(item_list, price_list, rating_list), columns=['ProductName','Price', 'Rating'])


# In[136]:


# Adjust the Price Col
def clean_data(data):
    data = data.replace('$', '').replace('%', '')
    amount_change = data.split('\n')
    amount = float(amount_change[0])
    change = int(amount_change[1]) if len(amount_change) > 1 else None
    return amount, change

df1[['Product_Price', 'Price_Discount_Rate']] = pd.DataFrame(df1['Price'].apply(clean_data).tolist(), index=df1.index)


# In[137]:


# Adjust the Rating Col
def clean_data_v2(data):
    data = data.replace('(', '').replace(')', '').replace('+','')
    return data

df1[['Min_Rating']] = pd.DataFrame(df1['Rating'].apply(clean_data_v2).tolist(), index=df1.index)


# In[138]:


# Define the product type by Keywords at Title
def product_identifier(text):
    if 'T-shirt' in text or 'T-Shirt' in text:
        return 'T-Shirt'
    elif 'Bikini' in text:
        return 'Bikini'
    elif 'Cardigan' in text:
        return 'Cardigan'
    elif 'Vest' in text:
        return 'Vest'
    elif 'Pants' in text:
        return 'Pants'
    elif 'Crop' in text:
        return 'Crop'
    elif 'Tee' in text:
        return 'Tee'
    elif 'Top' in text and 'Short' in text:
        return 'Top & Shorts'
    elif 'Top' in text or 'TOP' in text:
        return 'Top'
    elif 'Shirt' in text:
        return 'Shirt'
    elif 'Blouse' in text:
        return 'Shirt'
    elif 'Camisole' in text:
        return 'Camisole'
    elif 'Shorts' in text:
        return 'Shorts'
    elif 'Jumpsuit' in text:
        return 'Jumpsuit'
    elif 'Jeans' in text:
        return 'Jeans'
    elif 'Tank' in text:
        return 'Tank'
    elif 'Dress' in text:
        return 'Dress'
    else:
        return 'Others'

df1['Product_Type'] = df1['ProductName'].apply(product_identifier)
df1


# In[139]:


# Define the Markets by Keywords at Title
def market_identifier(text):
    if 'SHEIN EZwear' in text:
        return 'SHEIN EZwear'
    elif 'SHEIN Essnce' in text:
        return 'SHEIN Essnce'
    elif 'SHEIN LUNE' in text:
        return 'NEW SHEIN LUNE'
    elif 'SHEIN Slayr' in text:
        return 'NEW SHEIN LUNE'
    elif 'MUSERA' in text:
        return 'MUSERA'
    elif 'SHEIN MOD' in text:
        return 'SHEIN MOD'
    elif 'SHEIN Clasi' in text:
        return 'SHEIN Clasi'
    elif 'SHEIN BAE' in text:
        return 'SHEIN BAE'
    elif 'SHEIN Privé' in text:
        return 'SHEIN Privé'
    elif 'SHEIN Frenchy' in text:
        return 'SHEIN Frenchy'
    elif 'SHEIN Swim' in text:
        return 'SHEIN Swim'
    elif 'SHEIN JORESS' in text:
        return 'SHEIN JORESS'
    elif 'SHEIN VCAY' in text:
        return 'SHEIN VCAY'
    elif 'EMERY ROSE' in text:
        return 'EMERY ROSE'
    elif 'SHEIN Aloruh' in text:
        return 'SHEIN Aloruh'
    elif 'SHEIN Qutie' in text:
        return 'SHEIN Qutie'
    elif 'SHEIN LONESS' in text:
        return 'SHEIN LONESS'
    elif 'SHEIN WYWH' in text:
        return 'SHEIN WYWH'
    elif 'SHEIN Coolane' in text:
        return 'SHEIN Coolane'
    elif 'Acelitt' in text:
        return 'Acelitt'
    else:
        return 'Others'

df1['Market_Name'] = df1['ProductName'].apply(market_identifier)
df1


# In[140]:


# Define the Products Either its New or Not by Keyword
def new_identifier(text):
    if 'NEW' in text or 'New' in text or 'new' in text:
        return 'YES'
    else:
        return 'NO'

df1['Product_New'] = df1['ProductName'].apply(new_identifier)
df1


# In[141]:


import numpy as np
def empty_data(data):
    # Eğer veri boş string, None veya NaN ise NaN ile değiştir
    if data == '' or data is None or pd.isna(data):
        return np.nan
    return data
df1[['Min_Rate']] = pd.DataFrame(df1['Min_Rating'].apply(empty_data).tolist(), index=df1.index)
df1


# In[142]:


df2 = df1[['ProductName', 'Product_Price', 'Price_Discount_Rate', 'Product_Type', 'Market_Name', 'Product_New', 'Min_Rate']]
df2


# In[144]:


df2.to_excel('shein_data.xlsx', index=False)

