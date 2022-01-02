from bs4 import BeautifulSoup
import requests
import os
import subprocess

class NyaaScraper:
    SUBBED = '2'
    RAW = '3'

    def __init__(self):
        # anime from trusted uploaders
        self.source = 'https://nyaa.si'
        self.reqDelay = 1

    def scrape(self, title, isSubbed):
        url = self.constructURL(title, isSubbed)
        rawHtml = requests.get(url).text
        soup = BeautifulSoup(rawHtml, 'lxml')
        entry = soup.find('tr', class_ = 'success')
        return entry

    def constructURL(self, title, isSubbed):
        url = f'{self.source}/?f=2&c=1_$SUB&q=$TITLE'
        url = url.replace('$TITLE', title)
        url = url.replace('$SUB', self.SUBBED if isSubbed else self.RAW)
        return url

    def extractData(self, entry):
        columns = entry.findAll('td')
        title = self.extractTitle(columns[1])
        downloadLink = self.extractDownloadLink(columns[2])
        magnetLink = self.extractMagnetLink(columns[2])
        data = list(map(lambda col: col.text, columns[3:8]))
        size = data[0]
        date = data[1]
        seeders = data[2]
        leechers = data[3]
        completedDownloads = data[4]
        return [title, downloadLink, magnetLink, size, date, seeders, leechers, completedDownloads]

    def extractTitle(self, column):
        return column.findAll('a')[-1].text

    def extractDownloadLink(self, column):
        downloadExtension = column.findAll('a')[0]['href']
        return f'{self.source}{downloadExtension}'

    def extractMagnetLink(self, column):
        return column.findAll('a')[1]['href']

scraper = NyaaScraper()
print(scraper.extractData(scraper.scrape('jujutsu kaisen', True)))