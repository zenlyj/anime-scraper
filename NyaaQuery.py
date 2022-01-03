import sys

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

    def getUploader(self, entry):
        name = entry.split(',')[0]
        uploader = name.split(' ')[0]
        uploader = uploader[1 : len(uploader)-1]
        return uploader

print(NyaaQuery('db.csv').getUploaders())