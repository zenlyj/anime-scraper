import sys
import math

class NyaaQuery:
    def __init__(self, path):
        try:
            f = open(path, 'rt')
            self.path = path
            self.data = self.deserialize(f)
        except FileNotFoundError:
            sys.exit('File does not exist')

    def deserialize(self, file):
        entries = []
        for line in file:
            entries.append(line)
        file.close()
        return entries

    def getUploaders(self):
        uploaders = set()
        for entry in self.data:
            uploader = self.getUploader(entry)
            uploaders.add(uploader)
        return list(uploaders)

    def filterByUploader(self, uploader):
        return list(filter(lambda entry : True if self.getUploader(entry).lower() == uploader.lower() else False, self.data))

    def sortByDownloads(self, isDsc):
        return sorted(self.data, key = lambda x : int(x.split(',')[7]), reverse=isDsc)

    def sortByLeechers(self, isDsc):
        return sorted(self.data, key = lambda x : int(x.split(',')[6]), reverse=isDsc)

    def sortBySeeders(self, isDsc):
        return sorted(self.data, key = lambda x : int(x.split(',')[5]), reverse=isDsc)

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
        return sorted(self.data, key = lambda x : comparator(x.split(',')[3]), reverse=isDsc)

    def getUploader(self, entry):
        name = entry.split(',')[0]
        uploader = name.split(' ')[0]
        uploader = uploader[1 : len(uploader)-1]
        return uploader

for i in NyaaQuery('db.csv').sortBySeeders(True):
    print(i)