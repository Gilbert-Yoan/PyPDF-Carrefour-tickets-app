from .sqlHandler import Initializer, Inserter, Loader, Session, Editer
from . import FileSystem, Reader

class Controller():

    def __init__(self):
        self.initializer = Initializer.Initializer(self)
        self.inserter = Inserter.Inserter(self)
        self.session = Session.Session(self, 'product.db')
        self.loader = Loader.Loader(self)
        self.editer = Editer.Editer(self)
        self.filesystem = FileSystem.FileSystem()
        self.reader = Reader.Reader(self)
