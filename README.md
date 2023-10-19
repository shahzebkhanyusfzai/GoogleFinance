![Header Image](https://drive.google.com/uc?export=view&id=1dx4iV9hw7IsNUzls4K5iG0M1PPQz7z7I)

# Google Finance Time Series Scraper
This repo elaborates on how can we scrape the ticker time series data (like the screenshot below) from Google Finance.

<img src="https://drive.google.com/uc?export=view&id=1gbk210OvwVIS5zel8PSlY-cFQJZ6lKwe" width="800"/>


## Table of Contents
1. [Introduction](#introduction)
2. [Environment Setup](#environment-setup)
3. [Code Walkthrough](#code-walkthrough)
    - [Imports](#imports)
    - [Utility Functions](#utility-functions)
    - [Core Function](#core-function)
4. [Execution](#execution)
5. [Results](#results)
6. [Potential Use](#potential-use)
7. [Full Code](#full-code)
8. [Support](#support)

## Introduction
A robust scraper to retrieve time series data for tickers from Google Finance. This tool scrapes price, date, and volume details providing a detailed analysis capability for the selected tickers.

## Environment Setup
```bash
pip install webdriver-manager scrapy selenium pandas
```
## Code Walkthrough

### Imports

```python
from webdriver_manager.chrome import ChromeDriverManager
from scrapy import Selector
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
```

## Utility Functions

### Getting the Web Driver
This function is responsible for setting up and returning a web driver using Chrome. The driver will be used to navigate to web pages and interact with them programmatically.
```python
def getdriver():
    options = Options()
    # options.headless = True
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    return driver
```

### Rearrange String for Ticker
Given a ticker string in the format "EXCHANGE: TICKER", this function swaps the order to "TICKER: EXCHANGE". This rearrangement is necessary to construct the correct URL for fetching the desired stock data from Google Finance.
```python
def rearrange_string(text):
  parts = text.split(':')
  symbol = parts[1].strip()
  exchange = parts[0].strip()
  return f"{symbol}:{exchange}"
```

### Export Data to CSV
This function handles the exporting of scraped data to a CSV file. On its first call, it writes a new CSV file with headers. On subsequent calls, it appends data without repeating the headers.
```python
switch = True
def exporter(row):
    file_name = 'data.csv'
    global switch 
    if switch:
        switch = False
        pd.DataFrame(row,index=[0]).to_csv(file_name,index=False,mode='a')
    else:
        pd.DataFrame(row,index=[0]).to_csv(file_name,index=False,mode='a',header=False)
```

## Core Function
### Scraping Time Series Graph

Scraping Time Series Graph
This function interacts with Google Finance's graphical interface to scrape time series data points for a given ticker. By simulating mouse movements over the graph, it captures price, date, and volume information for the desired timeframe. The timeframe can be changed under the timeframe variable as per your need from any of the following values '1D','5D','1M','6M','YTD','1Y','5Y','MAX'

```python
def scraping_time_series_graph(driver):
    data_points = []
    time.sleep(4)
    try:
        graph = driver.find_element(By.XPATH,"//*[name()='svg']/*[name()='g']/descendant::*[name()='g'][@class='gJBfM']")
    except:
        pass
    time.sleep(2)
    try:
        for x in range(-325, 325):
            action = ActionChains(driver).move_to_element_with_offset(graph, x, graph.size['height'] / 2)
            action.perform()
            response = Selector(text=driver.page_source)
            price = response.xpath("//div[@class='hSGhwc']/p[@jsname='BYCTfd']/text()").get()
            date = response.xpath("//div[@class='hSGhwc']/p[@jsname='LlMULe']/text()").get()
            volume = response.xpath("//div[@class='hSGhwc']/p[@jsname='R30goc']/span/text()").get()
            
            data = {
                'price': price,
                'date': date,
                'volume': volume
            }

            data_points.append(data)
            exporter(data)
        print(data_points)
        return data_points

    except:
        data_points = ''

our_tickers = [
    'KLSE: VITROX',
    'KLSE: GTRONIC',
    'KLSE: FRONTKN',
    'KLSE: MQTECH',
    'KLSE: KESM',
    'KLSE: PENTA',
    'KLSE: GREATEC',
]

driver = getdriver()
timeframe = '5Y'       # i.e '1D','5D','1M','6M','YTD','1Y','5Y','MAX'
for ticker in our_tickers:
    ticker = rearrange_string(ticker)
    driver.get(f'https://www.google.com/finance/quote/{ticker}?hl=en&window={timeframe}')
    driver.maximize_window()
    scraping_time_series_graph(driver)
```


## Execution
Ensure you have the necessary environment set up. Use the utility functions to streamline your scraping process. Execute the scraping_time_series_graph function to begin the data collection.

GIFs of Working Selenium Drivers and Output CSV Files:
![Selenium Driver GIF](https://imgur.com/TI9p8Ky.gif)


## Results
Example rows from the CSV data:

| Date   | Price | Volume |
|--------|-------|--------|
| 1-Mar-19 | MYR RM3.51 | 2M |
| 8-Mar-19 | MYR RM3.64 | 4.2M |
| 15-Mar-19 | MYR RM3.61 | 1.3M |
| 22-Mar-19 | MYR RM3.61 | 1.3M |
| 29-Mar-19 | MYR RM3.59 | 701K |
| 5-Apr-19 | MYR RM3.58 | 3.1M |
| 12-Apr-19 | MYR RM3.54 | 878K |
.
.
.


## Potential Use
Custom Visualizations: Users can create customized dashboards and visualizations based on the data collected.
Data Analysis: Helps in forecasting and analyzing stock market trends.
Portfolio Management: Allows users to have a detailed insight into their stocks' past performance.

## Full Code
```python
from webdriver_manager.chrome import ChromeDriverManager
from scrapy import Selector
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def getdriver():
    options = Options()
    # options.headless = True
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    return driver

def rearrange_string(text):
  parts = text.split(':')
  symbol = parts[1].strip()
  exchange = parts[0].strip()
  return f"{symbol}:{exchange}"

switch = True
def exporter(row):
    file_name = 'data.csv'
    global switch 
    if switch:
        switch = False
        pd.DataFrame(row,index=[0]).to_csv(file_name,index=False,mode='a')
    else:
        pd.DataFrame(row,index=[0]).to_csv(file_name,index=False,mode='a',header=False)

def scraping_time_series_graph(driver):
    data_points = []
    time.sleep(4)
    try:
        graph = driver.find_element(By.XPATH,"//*[name()='svg']/*[name()='g']/descendant::*[name()='g'][@class='gJBfM']")
    except:
        pass
    time.sleep(2)
    try:
        for x in range(-325, 325):
            action = ActionChains(driver).move_to_element_with_offset(graph, x, graph.size['height'] / 2)
            action.perform()
            response = Selector(text=driver.page_source)
            price = response.xpath("//div[@class='hSGhwc']/p[@jsname='BYCTfd']/text()").get()
            date = response.xpath("//div[@class='hSGhwc']/p[@jsname='LlMULe']/text()").get()
            volume = response.xpath("//div[@class='hSGhwc']/p[@jsname='R30goc']/span/text()").get()
            
            data = {
                'price': price,
                'date': date,
                'volume': volume
            }

            data_points.append(data)
            exporter(data)
        print(data_points)
        return data_points

    except:
        data_points = ''

our_tickers = [
    'KLSE: VITROX',
    'KLSE: GTRONIC',
    'KLSE: FRONTKN',
    'KLSE: MQTECH',
    'KLSE: KESM',
    'KLSE: PENTA',
    'KLSE: GREATEC',
]

driver = getdriver()
timeframe = '5Y'       # i.e '1D','5D','1M','6M','YTD','1Y','5Y','MAX'
for ticker in our_tickers:
    ticker = rearrange_string(ticker)
    driver.get(f'https://www.google.com/finance/quote/{ticker}?hl=en&window={timeframe}')
    driver.maximize_window()
    scraping_time_series_graph(driver)
```

If you'd like to contribute or suggest future enhancements, feel free to raise issues or make pull requests.

## Support
Loved the scraper? Consider supporting by buying me a coffee!

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/shahzeb)


