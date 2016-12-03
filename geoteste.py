import os
import sys
import math
import json 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from geopy import geocoders
import redis





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



import unittest

class TestTrataGeo(unittest.TestCase):
    
    def test_deg2rad(self):
        t = TrataGeo()
        self.assertEqual(round(t.deg2rad(10), 2), 0.17)
        

    def test_rad2deg(self):
        t = TrataGeo()
        self.assertEqual(round(t.rad2deg(0.17), 2), 9.74)


if __name__ == "__main__":
    unittest.main()