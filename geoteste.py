import os
import sys
import math
import json 
import doctest
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from geopy import geocoders
import redis


#Change them with your authotenfication tokens
ckey = 'B4qL5xWeoAtT4HDeM8fPRTUau'
csecret ='XpctNz94QrAmv7ybKHNS70TK9DhD8LBadFNo4Rv3rxQlR1e7bd'
atoken = '138579781-WdFq2TX2MSIW1Gh8JsQzY4iWqaO032TLVqUVjhSc'
asecret = 'yHE559wpPnHJmFzeFY9JOHSUO5zSQhxGhJnZcGNEOWArR'
#################################


class RedisInterface():

    conn = None

    def connect(self, host, port, db):
        self.conn = redis.StrictRedis(host=host, port=port, db=db)

    def grafaDados(self, data):
        self.conn.set(data['text'], data['coordinates'])

class listener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        if data['coordinates']!=None:
            chaves = ['text', 'coordinates']
            data_formatada = {}
            for i in chaves:
                if data.__contains__(i):	
                    if i == 'coordinates':
                        data_formatada[i] = json.dumps(data[i]['coordinates'])
                    else:
                        data_formatada[i] = data[i]
            print data_formatada
            red = RedisInterface()
            red.connect(host='localhost', port=6379, db=0)
            red.grafaDados(data_formatada)
            #print >>logfile, stream_log
            
        else:
            print "Sem geo"
        return True

    def on_error(self, statut):
        print statut
        
class TrataGeo():
    
    # Semi-axes of WGS-84 geoidal reference
    __WGS84_a = 6378137.0  # Major semiaxis [m]
    __WGS84_b = 6356752.3  # Minor semiaxis [m]
    
    
    # degrees to radians
    def deg2rad(self, degrees):
        '''
        >>> t = TrataGeo()
        >>> rad = t.deg2rad(10)
        >>> grad = t.rad2deg(rad)
        10
        '''
        return math.pi*degrees/180.0
    # radians to degrees
    def rad2deg(self, radians):
        return 180.0*radians/math.pi
    
    # Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
    def WGS84EarthRadius(self, lat):
        # http://en.wikipedia.org/wiki/Earth_radius
        An = self.__WGS84_a * self.__WGS84_a * math.cos(lat)
        Bn = self.__WGS84_b * self.__WGS84_b * math.sin(lat)
        Ad = self.__WGS84_a * math.cos(lat)
        Bd = self.__WGS84_b * math.sin(lat)
        return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )
    
    # Bounding box surrounding the point at given coordinates,
    # assuming local approximation of Earth surface as a sphere
    # of radius given by WGS84
    def bounding_box(self, latitudeInDegrees, longitudeInDegrees, halfSideInKm):
        lat = self.deg2rad(latitudeInDegrees)
        lon = self.deg2rad(longitudeInDegrees)
        halfSide = 1000*halfSideInKm
    
        # Radius of Earth at given latitude
        radius = self.WGS84EarthRadius(lat)
        # Radius of the parallel at given latitude
        pradius = radius*math.cos(lat)
    
        latMin = lat - halfSide/radius
        latMax = lat + halfSide/radius
        lonMin = lon - halfSide/pradius
        lonMax = lon + halfSide/pradius
    
        return (self.rad2deg(latMin), self.rad2deg(lonMin), self.rad2deg(latMax), self.rad2deg(lonMax))

def main():
    
    adress=str(sys.argv[1]) #Location (City name, adress...)
    halfradius=float(sys.argv[2]) #Radius in Km of the Bounding Box
    g = geocoders.GoogleV3()
    place, (lat, lng) = g.geocode(adress)
    geo = TrataGeo()
    location = [geo.bounding_box(lng,lat,halfradius)[0],geo.bounding_box(lng,lat,halfradius)[1],geo.bounding_box(lng,lat,halfradius)[2],geo.bounding_box(lng,lat,halfradius)[3]]
    # print "Location of "+ adress+" :",lng,lat
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=location)
    
   
main()
