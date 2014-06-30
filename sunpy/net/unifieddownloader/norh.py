from sunpy.net.vso.attrs import Time, Instrument
from sunpy.net.unifieddownloader.client import GenericClient
import datetime,urlparse

__all__ = ['Time', 'Instrument']
class NoRHClient(GenericClient):
    
    def _get_url_from_timerange(cls, timerange, **kwargs):
        days = timerange.get_days()
        urls = []
        for day in days:
            urls.append(cls._get_url_for_date(day, **kwargs))
        return urls

    def _get_url_for_date(cls, date, **kwargs):
        """This method retrieves the url for NoRH correlation data for the given date."""

        # Hack to get around Python 2.x not backporting PEP 3102.
        wavelength = kwargs.pop('wavelength', None)

        #default urllib password anonymous@ is not accepted by the NoRH FTP server.
        #include an accepted password in base url
        baseurl='ftp://anonymous:mozilla@example.com@solar-pub.nao.ac.jp/pub/nsro/norh/data/tcx/'

        #date is a datetime.date object
        if wavelength == '34':
            final_url=urlparse.urljoin(baseurl,date.strftime('%Y/%m/' + 'tcz' + '%y%m%d'))
        else:
            final_url=urlparse.urljoin(baseurl, date.strftime('%Y/%m/' + 'tca' + '%y%m%d'))

        return final_url

    def _makeimap(self):
       '''map_:Dict'''
       self.map_['source']= 'NAOJ'
       self.map_['provider'] ='NRO'
       self.map_['instrument'] = 'RadioHelioGraph'
       self.map_['phyobs'] = ''
    
    @classmethod
    def _can_handle_query(cls,*query):
        
	chkattr =  ['Time','Instrument']
        chklist =  [x.__class__.__name__ in chkattr for x in query]
        for x in query:
	    if x.__class__.__name__ == 'Instrument' and x.value == 'norh':
                return all(chklist)
	return False
 