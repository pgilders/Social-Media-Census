#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:15:18 2019

@author: Patrick
"""

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
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time
import re

# All(?) the country codes (212).
# Long, but have provided in this format to be more editable / readable. Alternatively store in txt and import.
countries = {'Africa': ['Algeria',
  'Angola',
  'Benin',
  'Botswana',
  'Burkina Faso',
  'Burundi',
  'Cameroon',
  'Cape Verde',
  'Central African Republic',
  'Chad',
  'Comoros',
  'Democratic Republic of the Congo',
  'Djibouti',
  'Egypt',
  'Equatorial Guinea',
  'Eritrea',
  'Ethiopia',
  'Gabon',
  'Ghana',
  'Guinea',
  'Kenya',
  'Lesotho',
  'Libya',
  'Madagascar',
  'Malawi',
  'Mali',
  'Mauritania',
  'Mauritius',
  'Mayotte',
  'Morocco',
  'Mozambique',
  'Namibia',
  'Niger',
  'Nigeria',
  'Republic of the Congo',
  'Rwanda',
  'Réunion',
  'Sao Tome and Principe',
  'Senegal',
  'Seychelles',
  'Sierra Leone',
  'Somalia',
  'South Africa',
  'Swaziland',
  'Tanzania',
  'The Gambia',
  'Togo',
  'Tunisia',
  'Uganda',
  'Zambia',
  'Zimbabwe'],
 'Europe': [
         'Aland Islands',
  'Albania',
  'Andorra',
  'Austria',
  'Belarus',
  'Belgium',
  'Bosnia and Herzegovina',
  'Bulgaria',
  'Croatia',
  'Cyprus',
  'Czech Republic',
  'Denmark',
  'Estonia',
  'Faroe Islands',
  'Finland',
  'France',
  'Germany',
  'Gibraltar',
  'Greece',
  'Guernsey',
  'Hungary',
  'Iceland',
  'Ireland',
  'Isle Of Man',
  'Italy',
  'Jersey',
  'Latvia',
  'Liechtenstein',
  'Lithuania',
  'Luxembourg',
  'Macedonia',
  'Malta',
  'Moldova',
  'Monaco',
  'Montenegro',
  'Netherlands',
  'Norway',
  'Poland',
  'Portugal',
  'Romania',
  'Russia',
  'San Marino',
  'Serbia',
  'Slovakia',
  'Slovenia',
  'Spain',
  'Sweden',
  'Switzerland',
  'Ukraine',
  'United Kingdom',
  'Vatican City'
  ],
 'South America': ['Argentina',
  'Bolivia',
  'Brazil',
  'Chile',
  'Colombia',
  'Ecuador',
  'Falkland Islands',
  'French Guiana',
  'Guyana',
  'Paraguay',
  'Peru',
  'Suriname',
  'Uruguay',
  'Venezuela'],
 'North America': ['Bermuda', 'Canada', 'Greenland', 'United States'],
 'Asia': ['Afghanistan',
  'Armenia',
  'Azerbaijan',
  'Bahrain',
  'Bangladesh',
  'Bhutan',
  'Brunei',
  'Cambodia',
  'China',
  'Georgia',
  'Hong Kong',
  'India',
  'Indonesia',
  'Iraq',
  'Israel',
  'Japan',
  'Jordan',
  'Kazakhstan',
  'Kuwait',
  'Kyrgyzstan',
  'Laos',
  'Lebanon',
  'Macau',
  'Malaysia',
  'Maldives',
  'Mongolia',
  'Nepal',
  'Oman',
  'Pakistan',
  'Palestine',
  'Philippines',
  'Qatar',
  'Saudi Arabia',
  'Singapore',
  'South Korea',
  'Sri Lanka',
  'Taiwan',
  'Tajikistan',
  'Thailand',
  'Turkey',
  'Turkmenistan',
  'United Arab Emirates',
  'Uzbekistan',
  'Vietnam',
  'Yemen'],
 'Oceania': [
  'American Samoa',
  'Australia',
  'Federated States of Micronesia',
  'Fiji',
  'French Polynesia',
  'Guam',
  'Kiribati',
  'Marshall Islands',
  'Nauru',
  'New Caledonia',
  'New Zealand',
  'Northern Mariana Islands',
  'Palau',
  'Papua New Guinea',
  'Samoa',
  'Solomon Islands',
  'Tonga',
  'Tuvalu',
  'Vanuatu'],
 'Caribbean': [
         'Anguilla',
  'Antigua',
  'Aruba',
  'Barbados',
  'British Virgin Islands',
  'Cayman Islands',
  'Dominica',
  'Dominican Republic',
  'Grenada',
  'Guadeloupe',
  'Haiti',
  'Jamaica',
  'Martinique',
  'Puerto Rico',
  'Saint Kitts and Nevis',
  'Saint Vincent and the Grenadines',
  'St. Lucia',
  'The Bahamas',
  'Trinidad and Tobago',
  'Turks and Caicos Islands',
  'US Virgin Islands'],
 'Central America': ['Belize',
  'Costa Rica',
  'El Salvador',
  'Guatemala',
  'Honduras',
  'Mexico',
  'Nicaragua',
  'Panama']}

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

continent_dict = {}

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
            
        
    
    
        try:
            driver.get(ads_URL) # navigate to audience insights page    
            driver.find_element_by_xpath("//div[@class='_4iyh _2pia _2pi4']//div[2]//button[1]").click() #'continue'
            
#            driver.find_element_by_xpath("//div[@class='_oon']//div//button[@class='_4-97 _xkk'][contains(text(),'Browse')]").click()
#            driver.find_element_by_xpath("//div[contains(text(),'Countries')]").click()
            
            
            
#            select = Select(driver.find_element_by_xpath("//div[@class='_oon']//div//button[@class='_4-97 _xkk'][contains(text(),'Browse')]"))

            # select by visible text
#            select.select_by_visible_text('Banana')
#            driver.find_element_by_xpath("//div[contains(text(),'Asia')]")
#            //div[contains(text(),'Asia')]
#            driver.find_element_by_xpath("//select[contains(text(),'Countries')]/option[text()='Asia']")
#
#            
#            driver.find_element_by_xpath("//li[@class='_4b90 _4b91 _4b92 _4b96']//span[@class='_2-st']")
            
            driver.find_element_by_xpath("//div[@data-testid='targeting_age_editor_min']").click()
            driver.find_element_by_xpath("//div[@class='_3leq'][contains(text(),'%d')]" %age).click()
            
            #            element = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div._10zm'), " monthly active people")) # wait til element loads, times out after 30s
            
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

pop_data = pd.DataFrame(index=range(18, 66), columns=[x for y in countries.values() for x in y])
ads_URL = 'https://www.facebook.com/adsmanager/creation?filter_set&act=%s' %account_id


while pop_data.isna().sum().sum()>0:
    try:
        chromedriver = '/usr/local/bin/chromedriver' # path to chrome driver
        driver = webdriver.Chrome(chromedriver) # start a browsing session
        driver.get('https://business.facebook.com/login/') # navigate to fb login page
        driver.find_element_by_id("email").send_keys(email) # enter authentication details
        driver.find_element_by_id("pass").send_keys(pwd)
        driver.find_element_by_id("loginbutton").click()
        wait = WebDriverWait(driver, 30) # Adjust timeout limit here. Reccommended to decrease this for a manageable overall scrape time.
        element = wait.until(EC.visibility_of_element_located((By.ID, 'contentCol'))) # wait for page to load, timeout after 30s - shouldn't happen
        driver.get(ads_URL) # navigate to audience insights page    
        driver.find_element_by_xpath("//div[@class='_4iyh _2pia _2pi4']//div[2]//button[1]").click() #'continue'
        
        countryerr = []
        for continent, country in countries.items():
#            if continent != 'North America':
#                continue
            time.sleep(3)
            for c in country:
                if c not in redo: #pop_data.isna().sum()[pop_data.isna().sum()>0].index:
                    continue
                print(c)
                counter=0
                try:
                    time.sleep(3)
                    driver.find_element_by_xpath("//div[@class='_5aj7']//i[@class='img sp_qJSUJQ6fhYB_2x sx_62e443']").click()
                except Exception as e:
                    print(e)
                    pass
                
                try:
                    time.sleep(1)
                    driver.find_element_by_xpath("//div[@class='_oon']//div//button[@class='_4-97 _xkk'][contains(text(),'Browse')]").click()
                    time.sleep(1)
                    driver.find_element_by_xpath("//div[contains(text(),'Countries')]").click()
                    time.sleep(1)
                    driver.find_element_by_xpath("//div[contains(text(),'%s')]" %continent).click()
                    time.sleep(1)
                    driver.find_element_by_xpath("//div[contains(text(),'%s')]" %c).click()
                except Exception as e:
                    print(e)
                    countryerr.append((continent, c))
                    continue
            
                try:    
                    driver.find_element_by_xpath("//div[@id='AGE']//div[2]").click()
                    driver.find_element_by_xpath("//div[@class='_3leq'][contains(text(),'18')]").click()
                except:
                    pass    
                
                for age in range(18, 66):
                    try:
                        if True:
                            driver.find_element_by_xpath("//div[@data-testid='targeting_age_editor_min']").click()
                            driver.find_element_by_xpath("//div[@class='_3leq'][contains(text(),'%d')]" %age).click()
                            dc=0
                            while True:
                                if dc>=10:
                                    raise IndexError
                                try:
                                    time.sleep(0.3)
                                    html = driver.page_source # get the page html
                                    soup = BeautifulSoup(html, "html5lib") # impotrt into beautifulsoup
                                    txt = soup.findAll("div", {"class":"_4fbp"})
                                    num = re.search('\d{0,3},?\d{3},?\d{0,3}', txt[0].text)[0] # get the population description text
                                    break
                                except:
                                    dc+=1
                                    pass
                            print(c, age, pop_data.isna().sum().sum())   
                            pop_data.loc[age, c] = num
                            counter=0
                    except Exception as e:
                        counter+=1
                        print(e)
                        if counter>=3:
                            break
                pop_data.to_hdf('Downloads/popdata.h5', key='df', mode ='w')
        
        driver.quit() # exit session
    except KeyboardInterrupt:
#        break
        pass
    except Exception as e:
        print(e)
        driver.quit()
        pass
    
('Guinea', 'Equatorial Guinea')
('Guinea', 'Papua New Guinea')
('Niger', 'Nigeria')
('Republic of the Congo', 'Democratic Republic of the Congo')
('Samoa', 'American Samoa')
('Dominica', 'Dominican Republic')

redo=['Zimbabwe']
redo = ['Tanzania', 'Sierra Leone',  'Ethiopia',
        'Réunion', 'Mauritius', 'Namibia', 'Rwanda', 'Italy',
        'Andorra', 'Austria', 'Germany', 'France', 'Russia', 'Bosnia and Herzegovina',
        'Ireland', 'Sweden', 'Colombia', 'Ecuador', 'Qatar', 'Philippines', 'Armenia', 'Saudi Arabia',
        'Georgia', 'China', 'Australia', 'Uganda', 'Zambia', 'Iceland']
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
