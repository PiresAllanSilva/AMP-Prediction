from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd
import xerox
import time
from Bio import SeqIO

def portreports(file, driver_path, url = 'https://www.portoreports.com/stm'):
    with open(file) as f:
        fasta = f.read()
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    inputElement = driver.find_element_by_xpath('//*[@id="post-77"]/div/form/textarea')
    xerox.copy(fasta)
    inputElement.send_keys(Keys.CONTROL+ "v")
    inputElement.submit()
    content = driver.page_source
    soup = bs(content,features="lxml")
    driver.close()
    df = pd.read_html(soup.prettify())[0]
    return df.iloc[2: , :].reset_index(drop = True)

def dbaasp(file, driver_path, url = 'https://dbaasp.org/prediction/general'):
    with open(file) as f:
        fasta = f.read()
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    inputElement = driver.find_element_by_xpath('/html/body/main/div[2]/div/textarea')
    xerox.copy(fasta)
    inputElement.send_keys(Keys.CONTROL+ "v")
    driver.find_element_by_xpath('/html/body/main/div[2]/div/button').click()
    time.sleep(2)
    content = driver.page_source
    soup = bs(content,features="lxml")
    driver.close()
    df = pd.read_html(soup.prettify())[0]
    df.drop(df.tail(1).index,inplace=True)
    return df

def campr3(file, driver_path, url = 'http://www.camp.bicnirrh.res.in/predict/'):
    with open(file) as f:
        fasta = f.read()
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    inputElement = driver.find_element_by_xpath('//*[@id="frm1"]/p[1]/textarea')
    xerox.copy(fasta)
    inputElement.send_keys(Keys.CONTROL+ "v")
    driver.find_element_by_xpath('//*[@id="frm1"]/p[6]/label/input').click()
    inputElement.submit()
    content = driver.page_source
    soup = bs(content,features="lxml")
    driver.close()
    dfs = pd.read_html(soup.prettify())
    wanted = [dfs[3],dfs[4],dfs[6]]
    algos = ['SVM','RFC','ANN','DAC']
    count = 0
    for df in wanted:
        df['Algorithm'] = algos[count]
        count+=1
    return  pd.concat(wanted, ignore_index = True)

def ADAM(file, driver_path, url = 'http://bioinformatics.cs.ntou.edu.tw/ADAM/svm_tool.html'):
    with open(file) as f:
        fasta = f.read()
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    inputElement = driver.find_element_by_xpath('//*[@id="main2"]/form/center[1]/textarea')
    xerox.copy(fasta)
    inputElement.send_keys(Keys.CONTROL+ "v")
    inputElement.submit()
    content = driver.page_source
    soup = bs(content,features="lxml")
    driver.close()
    df = pd.read_html(soup.prettify())[1]
    df.columns = df.iloc[0]
    df.drop(df.index[0])
    return df.iloc[1: , :].reset_index(drop = True)
