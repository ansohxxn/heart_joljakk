import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from selenium import webdriver
import csv

# Get all internal links
def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    # Get list of all internal links (starts with link 'hyundai-poem/')
    for link in bsObj.findAll("a", href=re.compile("^(hyundai-poem/)")):
        # Links are not duplicated
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# Modify all internal links
def modifyUrl(listOfInternalLinks):
    fix_url = []
    inner_url = len(listOfInternalLinks)
    for inner_url in listOfInternalLinks:
        fix_url.append('http://woorimal.net/hangul/' + inner_url)  #extract each text 
    return fix_url

# Extract [title, poet, poem] from each internal link
def crawl_Poem(fix_url):
    text = len(fix_url)                                             
    listOfPoem = [[0 for i in range(3)] for j in range(text)]   
    row = 0

    driver = webdriver.Chrome(executable_path = "C:/Users/HYJ/Desktop/chromedriver/chromedriver.exe")
    for url in fix_url:
        driver.get(url)
        
        #시 제목
        title_element = "/html/body/table[1]/tbody/tr[1]/td/p/b/span"
        title = driver.find_element_by_xpath(title_element)
        title = (title.text).lstrip()
        listOfPoem[row][0] = title

        #시인
        poet_element = "/html/body/table[1]/tbody/tr[1]/td/p/span[1]"
        poet = driver.find_element_by_xpath(poet_element)
        poet = ((poet.text).replace(" ", "")).replace("-","")      #trim whitespaces
        listOfPoem[row][1] = poet

        #시
        poem_element1 = "/html/body/table[1]/tbody/tr[2]"
        poem_element2 = "/html/body/table[1]/tbody/tr[3]"
        
        poem1 = driver.find_element_by_xpath(poem_element1)
        poem1 = (poem1.text)
        listOfPoem[row][2] = poem1
        
        poem2 = driver.find_element_by_xpath(poem_element2)
        poem2 = (poem2.text)
        listOfPoem[row][2] = listOfPoem[row][2] + poem2

        row += 1
    driver.quit()
        
    return listOfPoem

# Shift data to csv file
def writeToCSV(results):
    data = pd.DataFrame(results)
    data.columns = ['시 제목', '시인', '시 본문']
    data.to_csv('시크롤링결과_정렬.csv', encoding='cp949')

def main():
    #1. Get url from website "woorimal.net" 
    url = "http://woorimal.net/hangul/hyundai%20poem-menu.htm"
    htm = urlopen(url)
    bsObj = BeautifulSoup(htm, "html.parser")

    #2. Get Internal link
    listOfInternalLinks = getInternalLinks(bsObj, htm)

    #3. Modify Internal link
    fix_url = []
    fix_url = modifyUrl(listOfInternalLinks)

    #4. Crawling each title, poet, poem from each internal link
    text = len(fix_url)                                             #total = 608 poems
    listOfPoem = [[0 for i in range(3)] for j in range(text)]       
    listOfPoem = crawl_Poem(fix_url)

    #5. Sort the list
    listOfPoem.sort(key=lambda x:x[0])
    
    #6. Write data to csv
    writeToCSV(listOfPoem)
      

if __name__=="__main__":
    main()  
