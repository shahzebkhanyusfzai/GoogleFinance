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
