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
from owslib.wcs import WebCoverageService

#from datetime import datetime

#start=datetime.now()
#print start

def get_wcs(server_url, spacename_wcs):

    chemin = '/home/tmp/'+spacename_wcs+'.tif'
    
    if not os.path.exists(chemin):
        
        wcs = WebCoverageService(server_url +"/wcs/",version='1.0.0')
    
        image = wcs[spacename_wcs]
        
        info = (image.boundingboxes)[0]
        
        epsg = info['nativeSrs']
        bboxx = info['bbox']
        
        offset = image.grid.offsetvectors
        cellsize_x= offset[0]
        x = cellsize_x[0]
        X = str(abs(float(x)))
        
        cellsize_y= offset[1]
        y = cellsize_y[1]
        Y = str(abs(float(y)))
        
#        img_formats = image.supportedFormats
#        img_format = img_formats[0]
        img_format = 'GeoTIFF'        
        
        print "Downloading the WCS: "+spacename_wcs
        print "From: "+server_url
        output = wcs.getCoverage(identifier = spacename_wcs,
                                 bbox = bboxx,
                                 crs = epsg,
                                 format = img_format,
                                 resx = X,
                                 resy = Y)                            
                                 
        data = output.read()
        f = open(chemin,'wb')
        f.write(data)
        f.close()
        print "Done"
    else: print "Done"
        
    return chemin

if __name__ == '__main__':
    get_wcs(sys.argv[1], sys.argv[2])
    

#server_url = "http://geoxxx.agrocampus-ouest.fr/geoserverwps/geouest"

#spacename_wcs = "geouest:Mosaic-Spot_2012"

#spacename_wcs = "geouest:spot_2012-09-09_up-r"

#spacename_wfs = "geouest:ROI_up-l"



#server_url = "http://geobretagne.fr/geoserver/ref"
#spacename_wcs = "ref:landsat_bretagne"