# -*- coding: utf-8 -*-
"""
This module contains cbrview for file contents
"""
import mimetypes
import zipfile
try:
    import tarfile
    TARMODULE_EXISTS = True
except:
    TARMODULE_EXISTS = False
try:
    import rarfile
    RARMODULE_EXISTS = True
except ImportError:
    RARMODULE_EXISTS = False
from Products.Five import BrowserView
from tempfile import NamedTemporaryFile
from collective.comicbookreader.config import BOOKS_MIMETYPES
import math

class CBRView(BrowserView):
    """
    Browserview that provides cbrview for file contents
    """

    def ceil(self, images, size):
        return int(math.ceil(images*1.0/size))

    def listImageFiles(self):
        ct = self.context.content_type
        tmp = NamedTemporaryFile()
        tmp.write(self.context.data)
        tmp.flush()
        fl = []
        if ct in BOOKS_MIMETYPES['zip']:
            fl = self.listZipFiles(tmp)
        if ct in BOOKS_MIMETYPES['tar']:
            fl = self.listTarFiles(tmp)
        if ct in BOOKS_MIMETYPES['rar']:
            fl = self.listRarFiles(tmp)
        return [{'filename': i, 'url': 'extract?fn=%s'% i} for i in fl]

    def is_image(self, name = ''):
        guessed_type = mimetypes.guess_type(name)
        if guessed_type[0] and guessed_type[0].startswith('image'):
            return True
        else:
            return False

    def listZipFiles(self, tmp_file):
        try:
            f = zipfile.ZipFile(tmp_file.name)
            return [i for i in f.namelist() if self.is_image(i)]
        except:
            return []
        
    def listRarFiles(self, tmp_file):
        try:
            f = rarfile.RarFile(tmp_file.name)
            return [i for i in f.namelist() if self.is_image(i)]
        except:
            return []

    def listTarFiles(self, tmp_file):
        try:
            f = tarfile.TarFile(tmp_file.name)
            return [i for i in f.getnames() if self.is_image(i)]
        except:
            return []
