import os
import logging
import geopy.geocoders
from geopy.geocoders import Nominatim
import urllib3
import json
import redis
from pathlib import Path

if os.getenv('ENVIRONMENT') == 'k8s':
    USER_AGENT = Path('/etc/worker-config-vol/geocoder.useragent').read_text()
    NREL_TOKEN = Path('/etc/worker-secret-vol/nrel.token').read_text()
    REDIS_HOST = Path('/etc/worker-config-vol/cache.svc').read_text()
else:
    USER_AGENT = os.getenv('EV_USER_AGENT')
    NREL_TOKEN = os.getenv('EV_NREL_TOKEN')
    REDIS_HOST = os.getenv('EV_REDIS_HOST')

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

class EVFinder(object):
    def __init__(self, config=None):
        if config:
            self.config = config
        else:
            self.config = {
                'STATIONS_NEAR_LOC_URL' : 'https://developer.nrel.gov/api/alt-fuel-stations/v1.json',
                'STATIONS_NEAR_ROUTE_URL' : 'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearby-route.json',
                'NREL_TOKEN' : NREL_TOKEN,
                'LIMIT' : '10',
                'USER_AGENT' : USER_AGENT
            }
        
    def set_location(self, query):
        try:
            query = str(query).strip().lower()

            if query:
                cached = r.hgetall(query.replace(' ','+'))

                if cached:
                    logging.debug('cache hit')
                    logging.debug(query)

                    self.zip            = cached.get('zip')
                    self.quarter        = cached.get('quarter')
                    self.neighbourhood  = cached.get('neighbourhood')
                    self.city           = cached.get('city')
                    self.state          = cached.get('state')
                    self.city_district  = cached.get('city_district')
                    self.suburb         = cached.get('suburb')

                    self.title = ' '.join([self.zip, self.quarter or '', self.neighbourhood or '', self.city or '', \
                                            self.city_district or '', self.suburb or '', self.state or ''])
                else:
                    logging.debug('cache miss')
                    logging.debug(query)

                    geopy.geocoders.options.default_user_agent = self.config.get('USER_AGENT')
                    geolocator = Nominatim() # or Nominatim(user_agent=self.config.get('USER_AGENT'))
                    location = geolocator.geocode(query=query, country_codes=['CA','US'], addressdetails=True)

                    if location:
                        logging.debug('\n\n' + str(location.raw) + '\n')
                        self.zip = location.raw.get('address').get('postcode')

                        # If the location is not precise enough to narrow it down to a ZIP code it's no good.
                        if self.zip:
                            self.quarter        = location.raw.get('address').get('quarter')
                            self.neighbourhood  = location.raw.get('address').get('neighbourhood')
                            self.city           = location.raw.get('address').get('city')
                            self.state          = location.raw.get('address').get('state')
                            self.city_district  = location.raw.get('address').get('city_district')
                            self.suburb         = location.raw.get('address').get('suburb')

                            self.title = ' '.join([self.zip, self.quarter or '', self.neighbourhood or '', self.city or '', \
                                                    self.city_district or '', self.suburb or '', self.state or ''])
                            logging.debug('\n\n'+ self.title + '\n')

                            r.hset(query.replace(' ','+'), mapping={
                                'zip' : self.zip,
                                'quarter' : self.quarter or '',
                                'neighbourhood' : self.neighbourhood or '',
                                'city' : self.city or '',
                                'state' : self.state or '',
                                'city_district' : self.city_district or '',
                                'suburb' : self.suburb or ''
                            })
                        else:
                            logging.debug(f'\n\nNo ZIP determined for: {query}\n')
                            r.hset(query.replace(' ','+'), mapping={'zip' : ''})
                        
        except Exception as e:
            logging.error(e)

    def get_stations(self):
        if hasattr(self,'zip') and self.zip:
            fields={'zip': self.zip,
                    'status': 'E',
                    'fuel_type': 'ELEC',
                    'limit': str(self.config.get('LIMIT'))}
            headers = {'X-Api-Key': self.config.get('NREL_TOKEN')}
            
            http = urllib3.PoolManager()
            response = http.request('GET', self.config.get('STATIONS_NEAR_LOC_URL'), fields=fields, headers=headers)
            
            return json.loads(response.data.decode("utf-8"))
        else:
            return None
