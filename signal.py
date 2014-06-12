class Signal(object):
    def __init__(self, name):
        self.name = name
        self.width = None
        self.direction = None
        self.parent = None
        self.active = None
        self.type = None
        self.logical_name = None
        self.constraints = None
        self.comments = None

    def __str__(self):
        pass


class CsvToBlock(object):
    def __init__(self):
        pass