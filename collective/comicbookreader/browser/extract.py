from Products.Five import BrowserView
import zipfile
from StringIO import StringIO
import mimetypes

class ExtractView(BrowserView):
    """ .. """

    def __call__(self):
        filename = self.request.form.get('fn',None)
        if filename:
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
            fname = filename.rsplit('/',1)[-1]
            self.request.response.setHeader("Content-disposition",mime_type)
            self.request.response.setHeader('Content-Disposition', 'attachment;filename=' + fname)
            self.request.response.setHeader("Content-type",mime_type)
            self.request.response.write(f.read())
        return self.request

    def is_zip(self):
        ct = self.context.content_type
        if ct == 'application/zip':
            return True
        else:
            return False
#        file_data = StringIO(self.context.data)
#        isZip = zipfile.is_zipfile(file_data)
#        return isZip

