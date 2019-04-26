import json
class JsonHelper(object):
    def __init__(self, fPath):
        with open(fPath, 'r') as inF:
            self.__dict__ = json.load(inF)
