import sys
from geopy import geocoders
from geoteste import TrataGeo, listener
from tweepy import OAuthHandler
from tweepy import Stream


#Change them with your authotenfication tokens
ckey = 'B4qL5xWeoAtT4HDeM8fPRTUau'
csecret ='XpctNz94QrAmv7ybKHNS70TK9DhD8LBadFNo4Rv3rxQlR1e7bd'
atoken = '138579781-WdFq2TX2MSIW1Gh8JsQzY4iWqaO032TLVqUVjhSc'
asecret = 'yHE559wpPnHJmFzeFY9JOHSUO5zSQhxGhJnZcGNEOWArR'
#################################


if __name__ == "__main__":
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