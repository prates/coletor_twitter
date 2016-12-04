# -*- coding: utf-8 -*-

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

help_str='''
Coletor de tweets. Desenvolvimento por Alexandre Prates
Modo de executar:

$ python exec.py "Cidade" "raio em relação ao centro da cidade" "linguagem"

Nome da cidade - Nome da ciodade que deseja coletar as twets, esse parametro é obrigatório
Raio em relação ao centro da cidade - essa é a distância em km do raio em relação ao coordenadas do centro da cidade, esse campo é obrigatório
linguagem - idioma da tweet, esse parametro eh opcional.

Exemplo de execucao;

$ python exec.py "São Paulo" 10 

Coleta as tweets da cidade de são paulo em um raio de 10 km.

$ python exec.py "São Paulo" 10 pt

Coleta as tweets da cidade de são paulo em um raio de 10 km com idioma portugues

'''



if __name__ == "__main__":
    argumentos = sys.argv
    if len(argumentos) > 1:
        if (len(argumentos) == 2 and ( argumentos[1] == "-h" or argumentos[1] == "--help" ) ):
            print help_str
        elif ( len(argumentos) > 2 and len(argumentos) < 5 ) :
            if len(argumentos) == 4:
                lang = argumentos[3]
            else:
                lang = None
            adress=str(argumentos[1]) #Location (City name, adress...)
            halfradius=float(argumentos[2]) #Radius in Km of the Bounding Box
            g = geocoders.GoogleV3()
            place, (lat, lng) = g.geocode(adress)
            geo = TrataGeo()
            location = [geo.bounding_box(lng,lat,halfradius)[0],geo.bounding_box(lng,lat,halfradius)[1],geo.bounding_box(lng,lat,halfradius)[2],geo.bounding_box(lng,lat,halfradius)[3]]
            # print "Location of "+ adress+" :",lng,lat
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitterStream = Stream(auth, listener(lang=lang))
            twitterStream.filter(locations=location)
        else:
            print "use a opção -h ou --help para opter ajuda."
        
    else:
        print "use a opção -h ou --help para opter ajuda."