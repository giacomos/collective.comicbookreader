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
    """ .. """

    def __call__(self):
        filename = self.request.form.get('fn',None)
        if not filename:
            return None
        ct = self.context.content_type
        data = None
        if ct in BOOKS_MIMETYPES['zip']:
            data = self.manageZip(filename)
        if ct in BOOKS_MIMETYPES['tar']:
            data = self.manageTar(filename)
        if ct in BOOKS_MIMETYPES['rar']:
            data = self.manageRar(filename)
        mime_type, tmp = mimetypes.guess_type(filename)
        if mime_type is None or not mime_type.startswith('image'):
            return None
        fname = filename.rsplit('/',1)[-1]
        if data:
            self.request.response.setHeader("Content-disposition",mime_type)
            self.request.response.setHeader('Content-Disposition', 'attachment;filename=' + fname)
            self.request.response.setHeader("Content-type",mime_type)
            self.request.response.write(data)
#        return self.request

    def manageZip(self, filename):
        try:
            file_data = StringIO(self.context.data)
            fz = zipfile.ZipFile(file_data)
            f = fz.open(filename)
        except zipfile.BadZipfile, e:
            return None
        except KeyError, e:
            return None
        mime_type, tmp = mimetypes.guess_type(filename)
        if mime_type is None or not mime_type.startswith('image'):
            return None
        return f.read()

    def manageRar(self, filename):
        if not RARMODULE_EXISTS:
            return None
        try:
            if len(self.context.data):
                tmp = NamedTemporaryFile()
                tmp.write(self.context.data)
                tmp.flush()
                frar = rarfile.RarFile(tmp.name)
                f = frar.open(filename)
                data = f.read()
                tmp.close()
                f.close()
                return data
        except:
            return None

    def manageTar(self, filename):
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
