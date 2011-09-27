from Products.Five import BrowserView
import zipfile
from StringIO import StringIO
import mimetypes

class CBRView(BrowserView):
    """ .. """

    def is_zip(self):
        ct = self.context.content_type
        if ct == 'application/zip':
            return True
        else:
            return False


    def getImgList(self, start = 0, size = 2):  
        file_data = StringIO(self.context.data)
        fz = zipfile.ZipFile(file_data)
        start = int(start)
        size = int(size)
        end = start + size
        names = fz.filelist[start:end]
        urls = [ "extract?fn=%s" % i.filename for i in names ]
        return urls

    def listImageFiles(self):
        try:
            file_data = StringIO(self.context.data)
            fz = zipfile.ZipFile(file_data)
            images = []
            for i in fz.filelist:
                if mimetypes.guess_type(i.filename)[0].startswith('image'):
                    images.append({'filename': i.filename, 'url': 'extract?fn=%s'% i.filename})
            return images
        except zipfile.BadZipfile, e:
            return []
