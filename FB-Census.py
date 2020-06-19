#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 09:13:43 2018

Performs a Facebook census, gathering the number of active users in each age bracket.
Scraping done with Selenium. Requires a browser driver installed.
Saves data to csv.

@author: Patrick Gildersleve - patrick.gildersleve ~at~ oii.ox.ac.uk
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import datetime
import pandas as pd

# All(?) the country codes (212).
# Long, but have provided in this format to be more editable / readable. Alternatively store in txt and import.
country_codes = ['US',
 'CA',
 'GB',
 'AR',
 'AU',
 'AT',
 'BE',
 'BR',
 'CL',
 'CN',
 'CO',
 'HR',
 'DK',
 'DO',
 'EG',
 'FI',
 'FR',
 'DE',
 'GR',
 'HK',
 'IN',
 'ID',
 'IE',
 'IL',
 'IT',
 'JP',
 'JO',
 'KW',
 'LB',
 'MY',
 'MX',
 'NL',
 'NZ',
 'NG',
 'NO',
 'PK',
 'PA',
 'PE',
 'PH',
 'PL',
 'RU',
 'SA',
 'RS',
 'SG',
 'ZA',
 'KR',
 'ES',
 'SE',
 'CH',
 'TW',
 'TH',
 'TR',
 'AE',
 'VE',
 'PT',
 'LU',
 'BG',
 'CZ',
 'SI',
 'IS',
 'SK',
 'LT',
 'TT',
 'BD',
 'LK',
 'KE',
 'HU',
 'MA',
 'CY',
 'JM',
 'EC',
 'RO',
 'BO',
 'GT',
 'CR',
 'QA',
 'SV',
 'HN',
 'NI',
 'PY',
 'UY',
 'PR',
 'BA',
 'PS',
 'TN',
 'BH',
 'VN',
 'GH',
 'MU',
 'UA',
 'MT',
 'BS',
 'MV',
 'OM',
 'MK',
 'LV',
 'EE',
 'IQ',
 'DZ',
 'AL',
 'NP',
 'MO',
 'ME',
 'SN',
 'GE',
 'BN',
 'UG',
 'GP',
 'BB',
 'AZ',
 'TZ',
 'LY',
 'MQ',
 'CM',
 'BW',
 'ET',
 'KZ',
 'NA',
 'MG',
 'NC',
 'MD',
 'FJ',
 'BY',
 'JE',
 'GU',
 'YE',
 'ZM',
 'IM',
 'HT',
 'KH',
 'AW',
 'PF',
 'AF',
 'BM',
 'GY',
 'AM',
 'MW',
 'AG',
 'RW',
 'GG',
 'GM',
 'FO',
 'LC',
 'KY',
 'BJ',
 'AD',
 'GD',
 'VI',
 'BZ',
 'VC',
 'MN',
 'MZ',
 'ML',
 'AO',
 'GF',
 'UZ',
 'DJ',
 'BF',
 'MC',
 'TG',
 'GL',
 'GA',
 'GI',
 'CD',
 'KG',
 'PG',
 'BT',
 'KN',
 'SZ',
 'LS',
 'LA',
 'LI',
 'MP', # Looks like here onward we get into some low population countries with no data in some age brackets.
 'SR', # 
 'SC',
 'VG',
 'TC',
 'DM',
 'MR',
 'AX',
 'SM',
 'SL',
 'NE',
 'CG',
 'AI',
 'YT',
 'CV',
 'GN',
 'TM',
 'BI',
 'TJ',
 'VU',
 'SB',
 'ER',
 'WS',
 'AS',
 'FK',
 'GQ',
 'TO',
 'KM',
 'PW',
 'FM',
 'CF',
 'SO',
 'MH',
 'VA',
 'TD',
 'KI',
 'ST',
 'TV',
 'NR',
 'RE']

### Runs selenium automated login and scraping of fb ads site (Javascript required). Ensure to have chrome driver (or alternative) installed

# Authentication details
email =''
pwd = ''
account_id = ''

imp = input('Would you like to import existing csvs? (Y/N)')

if imp.lower() in ['y', 'yes', 'true']:    
    # read csv(s) into df(s)
    print('Importing existing dataframes')
    dfpath = input('Enter path to text dataframe:')
    Ndfpath = input('Enter path to max numbers dataframe:')
    
    pop_data = pd.read_csv(dfpath) # create dataframe for population data (string)
    Npop_data = pd.read_csv(Ndfpath) # create dataframe for population data (number)
    
    # 
    c = input('Enter country code to start on:') 
    y = int(input('Enter age to start on:'))
    firstpass == True

else:
    print('Creating new dataframes')
    c = 'US'
    y = 18
    pop_data = pd.DataFrame(index=range(18, 66), columns=country_codes) # create dataframe for population data (string)
    Npop_data = pd.DataFrame(index=range(18, 66), columns=country_codes) # create dataframe for population data (number)
    firstpass == False    

error_list = []

chromedriver = '/usr/local/bin/chromedriver' # path to chrome driver
driver = webdriver.Chrome(chromedriver) # start a browsing session
driver.get('https://business.facebook.com/login/') # navigate to fb login page
driver.find_element_by_id("email").send_keys(email) # enter authentication details
driver.find_element_by_id("pass").send_keys(pwd)
driver.find_element_by_id("loginbutton").click()
wait = WebDriverWait(driver, 30) # Adjust timeout limit here. Reccommended to decrease this for a manageable overall scrape time.
element = wait.until(EC.visibility_of_element_located((By.ID, 'contentCol'))) # wait for page to load, timeout after 30s - shouldn't happen

timeout_counter = 0
for age in range(y, 66): # loop through ages
    
    if timeout_counter>=5: # Break if consecutive timeouts        
        try: # try to make simple connection, abort all scraping if not possible
            driver.get('https://www.facebook.com/ads/audience-insights/people?act=%s&age=18-18&country=US' %account_id) # attempt to navigate to audience insights page for US18   
            element = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div._10zm'), " monthly active people")) # wait til element loads, times out after 30s
            timeout_counter=0 # reset if loaded
        except TimeoutException: # abort if timeout on US18
            print("Connection to FB lost - scraping aborted")
            break
    
    for country in country_codes: # loop through countries
        
        if firstpass == True and country_codes.index(country) < country_codes.index(c): # 
            continue
        firstpass == False
            
        
        if timeout_counter>=5:
            try: # try to make simple connection, abort all scraping if not possible
                driver.get('https://www.facebook.com/ads/audience-insights/people?act=%s&age=18-18&country=US' %account_id) # attempt to navigate to audience insights page for US18   
                element = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div._10zm'), " monthly active people")) # wait til element loads, times out after 30s
                timeout_counter=0 # reset if loaded
            except TimeoutException: # abort if timeout on US18
                print("Connection to FB lost - scraping aborted")
                break     
            
        ads_URL = 'https://www.facebook.com/ads/audience-insights/people?act=%s&age=%d-%d&country=%s' %(account_id, age, age, country)
        
        try:
            driver.get(ads_URL) # navigate to audience insights page    
            element = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div._10zm'), " monthly active people")) # wait til element loads, times out after 30s
            
            html = driver.page_source # get the page html
            soup = BeautifulSoup(html, "html5lib") # impotrt into beautifulsoup
            txt = soup.findAll("div", {"class":"_10zm"})[0].text.split(' monthly')[0] # get the population description text
            
            lage = age
            lcountry = country
            print(age, country, txt)
            
            pop_data.loc[age, country] = txt # isolate the number and put in df  (still a string!)
            Npop_data.loc[age, country] = txt.split('–')[1]
            timeout_counter = 0 # reset timeout counter on completion
            
        except TimeoutException:
            print("Timed out - check connection or validate that data for country code %s exists" %country)
            
            pop_data.loc[age, country] = 0 # Set values as 0
            Npop_data.loc[age, country] = 0

            error_list.append((country, age))
            timeout_counter += 1

Npop_data = Npop_data.replace([r'[K]+$', r'[M]+$'], ['E+03', 'E+06'], regex=True).astype(float) #Convert strings to upper bound numbers
driver.quit() # exit session


### Handle any incomplete requests
p=''
if timeout_counter >= 5:
    print("Repeated consecutive timeouts, scraping aborted, check connection. Partial data being saved.")
    print("Errors:", error_list)
    p = "_(partial)"

elif len(error_list)>0:
    print("Timeouts for some data - check values", error_list)

print('Scraping aborted at: %s, %d.\nLast nonzero element: %s, %d' %(country, age, lcountry, lage))
   
### save data to csvs
filepath = '' #Where to save the results to 
date = datetime.datetime.today().strftime("%d-%m-%y") # datestamp

pop_data.to_csv(filepath+"popdata_%s.csv" %(date+p), sep = ',', header=True, index=True)
Npop_data.to_csv(filepath+"Npopdata_%s.csv" %(date+p), sep = ',', header=True, index=True)

print('Data Saved')
