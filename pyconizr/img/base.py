import os


class Image(object):

    def __init__(self, path):
        self.path = path
        self.filename = os.path.split(path)[1]
        self.name = os.path.splitext(self.filename)[0]
        self.width = self.height = 0

    def get_dimensions(self):
        return self.width, self.height

    def get_dataURI(self):
        """
        Returns the data URI for the image
        """
        return ''
