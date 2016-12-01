import os
import sys
import math
import time
from datetime import datetime
import json 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from geopy import geocoders
import redis

adress=str(sys.argv[1]) #Location (City name, adress...)
halfradius=float(sys.argv[2]) #Radius in Km of the Bounding Box
outputlocation=str(sys.argv[3])
datereq = datetime.utcnow().strftime("%d%m%Y")

#Change them with your authotenfication tokens
ckey = 'B4qL5xWeoAtT4HDeM8fPRTUau'
csecret ='XpctNz94QrAmv7ybKHNS70TK9DhD8LBadFNo4Rv3rxQlR1e7bd'
atoken = '138579781-WdFq2TX2MSIW1Gh8JsQzY4iWqaO032TLVqUVjhSc'
asecret = 'yHE559wpPnHJmFzeFY9JOHSUO5zSQhxGhJnZcGNEOWArR'
#################################


class redisInterface():

    conn = None

    def connect(self, host, port, db):
        self.conn = redis.StrictRedis(host=host, port=port, db=db)

    def grafaDados(self, data):
        self.conn.set(data['text'], data['coordinates'])

class listener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        logfile = open(os.path.join(outputlocation,adress+"-"+datereq+"-Request.csv"), "a")
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
            red = redisInterface()
            red.connect(host='localhost', port=6379, db=0)
            red.grafaDados(data_formatada)
            #print >>logfile, stream_log
            
        else:
            print "Sem geo"
        logfile.close()
        return True

    def on_error(self, statut):
        print statut

# degrees to radians
def deg2rad(degrees):
    return math.pi*degrees/180.0
# radians to degrees
def rad2deg(radians):
    return 180.0*radians/math.pi
# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis [m]
WGS84_b = 6356752.3  # Minor semiaxis [m]

# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
def WGS84EarthRadius(lat):
    # http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * math.cos(lat)
    Bn = WGS84_b*WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def boundingBox(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
    lat = deg2rad(latitudeInDegrees)
    lon = deg2rad(longitudeInDegrees)
    halfSide = 1000*halfSideInKm

    # Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat)
    # Radius of the parallel at given latitude
    pradius = radius*math.cos(lat)

    latMin = lat - halfSide/radius
    latMax = lat + halfSide/radius
    lonMin = lon - halfSide/pradius
    lonMax = lon + halfSide/pradius

    return (rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax))

def main():
    g = geocoders.GoogleV3()
    place, (lat, lng) = g.geocode(adress)
    location = [boundingBox(lng,lat,halfradius)[0],boundingBox(lng,lat,halfradius)[1],boundingBox(lng,lat,halfradius)[2],boundingBox(lng,lat,halfradius)[3]]
    # print "Location of "+ adress+" :",lng,lat
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=location)
main()
