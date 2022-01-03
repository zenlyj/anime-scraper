import sys
import math

class NyaaQuery:
    def __init__(self, path):
        try:
            f = open(path, 'rt')
            self.__data = self.__deserialize(f)
        except FileNotFoundError:
            sys.exit('File does not exist')

    def __deserialize(self, file):
        entries = []
        for line in file:
            entries.append(line)
        file.close()
        return entries

    def __getData(self):
        return self.__data

    def getNames(self):
        return list(map(lambda entry : entry.split(',')[0], self.__data))

    def getMagnetLinks(self):
        return list(map(lambda entry : entry.split(',')[2], self.__data))

    def getUploaders(self):
        uploaders = set()
        for entry in self.__data:
            uploader = self.__getUploader(entry)
            uploaders.add(uploader)
        self.__data = list(uploaders)

    def filterByUploader(self, uploader):
        self.__data = list(filter(lambda entry : True if self.__getUploader(entry).lower() == uploader.lower() else False, self.__data))

    def filterByQuality(self, quality):
        self.__data = list(filter(lambda entry : True if self.__getQuality(entry) == quality.lower() else False, self.__data))

    def sortByName(self, isDsc):
        self.__data = sorted(self.__data, key = lambda x : x.split(',')[0], reverse=isDsc)

    def sortByDownloads(self, isDsc):
        self.__data = sorted(self.__data, key = lambda x : int(x.split(',')[7]), reverse=isDsc)

    def sortByLeechers(self, isDsc):
        self.__data = sorted(self.__data, key = lambda x : int(x.split(',')[6]), reverse=isDsc)

    def sortBySeeders(self, isDsc):
        self.__data = sorted(self.__data, key = lambda x : int(x.split(',')[5]), reverse=isDsc)

    def sortBySize(self, isDsc):
        def comparator(size):
            split = size.split(' ')
            val = float(split[0])
            unit = split[1]
            power = 1
            if unit == 'KiB':
                power = 3
            elif unit == 'MiB':
                power = 6
            elif unit == 'GiB':
                power = 9
            return val * math.pow(10, power)
        self.__data = sorted(self.__data, key = lambda x : comparator(x.split(',')[3]), reverse=isDsc)

    def __getUploader(self, entry):
        name = entry.split(',')[0]
        uploader = name.split(' ')[0]
        uploader = uploader[1 : len(uploader)-1]
        return uploader

    def __getQuality(self, entry):
        name = entry.split(',')[0]
        if '[1080p]' in name or '(1080p)' in name:
            return '1080p'
        elif '[720p]' in name or '(720p)' in name:
            return '720p'
        elif '[480p]' in name or '(480p)' in name:
            return '480p'
        else:
            return None