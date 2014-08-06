import os


class Image(object):

    def __init__(self, path):
        self.path = path
        self.filename = os.path.split(path)[1]
        self.name = os.path.splitext(self.filename)[0]
        self.width = self.height = 0

    def get_dimensions(self):
        return self.width, self.height

    def set_dimensions(self, w, h):
        self.width = w
        self.height = h

    def data_type(self):
        raise NotImplementedError

    def encoded_URI(self):
        raise NotImplementedError

    def data_URI(self):
        """
        Returns the data URI for the image
        """
        return 'data:image/%s,%s' % (self.data_type(), self.encodedURI())
