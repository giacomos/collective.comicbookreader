# -*- coding: utf-8 -*-
"""
This module provides the view for images extraction
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
from StringIO import StringIO
from Products.Five import BrowserView
from tempfile import NamedTemporaryFile
from collective.comicbookreader.config import BOOKS_MIMETYPES

class ExtractView(BrowserView):
    """ Browserview that provides the view for images extraction
    """

    def __call__(self):
        filename = self.request.form.get('fn',None)
        index = self.request.form.get('i',None)
        if not filename and not index:
            return None
        ct = self.context.content_type
        data = None
        if ct in BOOKS_MIMETYPES['zip']:
            filename,data = self.manageZip(filename, index)
        if ct in BOOKS_MIMETYPES['tar']:
            filename, data = self.manageTar(filename, index)
        if ct in BOOKS_MIMETYPES['rar']:
            filename, data = self.manageRar(filename, index)
        if data:
            fname = filename.rsplit('/',1)[-1]
            guessed_type = mimetypes.guess_type(filename)
            self.request.response.setHeader('Content-Disposition', 'attachment;filename=' + fname)
            self.request.response.setHeader("Content-type", guessed_type[0])
            self.request.response.write(data)

    def is_image(self, name = ''):
        """ Returns True if the guessed mimetype is an image."""
        guessed_type = mimetypes.guess_type(name)
        if guessed_type[0] and guessed_type[0].startswith('image'):
            return True
        else:
            return False

    def manageZip(self, filename = None, index = None):
        """ Extracts data from zip archives """
        try:
            file_data = StringIO(self.context.data)
            fz = zipfile.ZipFile(file_data)
            images = [i for i in fz.namelist() if self.is_image(i)]
            if filename and filename not in images:
                return (None, None)
            name = filename and filename or images[int(index)]
            img = fz.open(name)
            return (name, img.read())
        except:
            return (None,None)

    def manageRar(self, filename = None, index = None):
        """ Extracts data from rar archives """
        if not RARMODULE_EXISTS:
            return None
        try:
            if len(self.context.data):
                tmp = NamedTemporaryFile()
                tmp.write(self.context.data)
                tmp.flush()
                frar = rarfile.RarFile(tmp.name)
                images = [i for i in frar.namelist() if self.is_image(i)]
                if filename and filename not in images:
                    return (None, None)
                name = filename and filename or images[int(index)]
                f = frar.open(name)
                data = f.read()
                tmp.close()
                f.close()
                return (name, data)
        except:
            return (None, None)

    def manageTar(self, filename = None, index = None):
        """ Extracts data from tar archives. """
        if not TARMODULE_EXISTS:
            return None
        try:
            if len(self.context.data):
                tmp = NamedTemporaryFile()
                tmp.write(self.context.data)
                tmp.flush()
                ftar = tarfile.TarFile(tmp.name)
                f = ftar.open(filename)
                data = f.read()
                tmp.close()
                f.close()
                return data
        except:
            return None
