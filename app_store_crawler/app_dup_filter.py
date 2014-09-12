from scrapy.dupefilter import RFPDupeFilter

class AppURLFilter(RFPDupeFilter):
    '''
        dup filter for url of app in google play
    '''
    def __getid__(self, url):
        '''
            remove same app in different languages
        '''
        url_piece=url.split('/')
        if len(url_piece)>4 and url_piece[4]=='app':
            if url_piece[3]=='us':
                self.fingerprints.add('/'.join(url_piece[4:]))
                return url
            else:
                return '/'.join(url_piece[4:])
        return url
    
    def request_seen(self, request):
        id=self.__getid__(request.url)
        if id in self.fingerprints:
            return True
        self.fingerprints.add(id)
#        if request.url.find('details?id=')>-1:
        print '[Filter]: have not seen', request.url
        if self.file:
            self.file.write(request.url)
            self.file.write('\n')
