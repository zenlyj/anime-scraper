from bs4 import BeautifulSoup
import requests
import os
import time

class NyaaScraper:
    __SUBBED = '2'
    __RAW = '3'

    def __init__(self):
        # anime from trusted uploaders
        self.source = 'https://nyaa.si'
        self.reqDelay = 1
        self.dataPath = 'scrapedData.csv'
        try:
            f = open(self.dataPath, 'wt')
        except FileNotFoundError:
            f = open(self.dataPath, 'xt')

    def __writeToFile(self, content):
        f = open(self.dataPath, 'at')
        f.write(content)
        f.close()

    def scrape(self, search, isSubbed):
        url = self.__constructURL(search, isSubbed, 1)
        rawHtml = requests.get(url).text
        soup = BeautifulSoup(rawHtml, 'lxml')
        buttonList = soup.find('ul', class_ = 'pagination')
        numPage = self.__extractNumPage(buttonList)
        self.__scrapeHelper(rawHtml)
        for i in range(2, int(numPage)+1):
            url = self.__constructURL(search, isSubbed, i)
            time.sleep(self.reqDelay)
            rawHtml = requests.get(url).text
            self.__scrapeHelper(rawHtml)
        
    def __scrapeHelper(self, rawHtml):
        soup = BeautifulSoup(rawHtml, 'lxml')
        entries = soup.findAll('tr', class_ = 'success')
        for entry in entries:
            data = self.__extractData(entry)
            # remove commas for csv formatting
            data = list(map(lambda x : x.replace(',', ''), data))
            self.__writeToFile(','.join(data) + '\n')

    def __constructURL(self, search, isSubbed, pageNum):
        url = f'{self.source}/?f=2&c=1_$SUB&q=$TITLE&p=$PAGENUM'
        url = url.replace('$TITLE', search)
        url = url.replace('$SUB', self.__SUBBED if isSubbed else self.__RAW)
        url = url.replace('$PAGENUM', str(pageNum))
        return url

    def __extractNumPage(self, buttonList):
        buttons = buttonList.findAll('li')
        # second last button is last page, last button is next button
        pageButton = buttons[len(buttons)-2]
        return pageButton.find('a').text

    def __extractData(self, entry):
        columns = entry.findAll('td')
        title = self.__extractTitle(columns[1])
        downloadLink = self.__extractDownloadLink(columns[2])
        magnetLink = self.__extractMagnetLink(columns[2])
        data = list(map(lambda col: col.text, columns[3:8]))
        size = data[0]
        date = data[1]
        seeders = data[2]
        leechers = data[3]
        completedDownloads = data[4]
        return [title, downloadLink, magnetLink, size, date, seeders, leechers, completedDownloads]

    def __extractTitle(self, column):
        return column.findAll('a')[-1].text

    def __extractDownloadLink(self, column):
        downloadExtension = column.findAll('a')[0]['href']
        return f'{self.source}{downloadExtension}'

    def __extractMagnetLink(self, column):
        return column.findAll('a')[1]['href']
