#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu May 01 22:33:15 2014

@author: Mounirsky
"""

#==============================================================================
# Ce module permet d'importer du geoserver une couche vecteur depuis un flux WFS 
# en utilisant l'adresse URL du server et le nom (ID) de la couche sur le geoserver.
# 
# Reference : https://github.com/geopython/OWSLib/tree/master/tests/doctests
#==============================================================================

import os
import sys
from owslib.wfs import WebFeatureService

#from datetime import datetime

#start=datetime.now()
#print start
    
def get_wfs(server_url, spacename_wfs):

    chemin = '/home/tmp/'+spacename_wfs+'.gml'

    if not os.path.exists(chemin):
        
        wfs = WebFeatureService(server_url +"/wfs/",version='1.0.0')
    
        vector = spacename_wfs
        
        print "Downloading the WFS: "+spacename_wfs
        print "From: "+server_url
        response = wfs.getfeature(typename =[vector])    
    
        data = response.read()
        f = open(chemin,'wb')
        f.write(data)
        f.close()
        print "Done"

    return chemin

if __name__ == '__main__':
    get_wfs(sys.argv[1], sys.argv[2])
    

#server_url = "http://geoxxx.agrocampus-ouest.fr/geoserverwps/geouest"

#spacename_wcs = "geouest:spot_2012-30-09_up-l"

#spacename_wcs = "geouest:spot_2012-09-09_up-r"

#spacename_wfs = "geouest:ROI_up-l"



#server_url = "http://geobretagne.fr/geoserver/ref"
#spacename_wcs = "ref:landsat_bretagne"