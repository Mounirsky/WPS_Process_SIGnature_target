#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 15:14:05 2014

@author: Mounir
"""
#==============================================================================
# Cette fonction permet de zipper un shapefile en utilisant le son nom,
# et supprimer tout les fichiers associés au vecteur après l'avoir zipper.
#==============================================================================

import os
import sys
import glob
import zipfile

def shapefile_zipper(inShapefile):
    
    os.chdir("/home/tmp/")
    
    newZipFN = 'zip_'+inShapefile[:-3] + 'zip'
    
    print 'Starting to Zip '+inShapefile+' to '+newZipFN
    
    if not (os.path.exists(inShapefile)):
        print inShapefile + ' Does Not Exist'
        return False
    
    if (os.path.exists(newZipFN)):
        print 'Deleting '+newZipFN
        os.remove(newZipFN)
    
    if (os.path.exists(newZipFN)):
        print 'Unable to Delete'+newZipFN
        return False
    
    bad_file = inShapefile[:-3] +"mshp"  
    
    if (os.path.exists(bad_file)):
        print 'Deleting '+bad_file
        os.remove(bad_file)  
    
    zipobj = zipfile.ZipFile(newZipFN,'w')
    
    for infile in glob.glob(inShapefile.replace(".shp",".*")):
        zipobj.write(infile,os.path.basename(infile),zipfile.ZIP_DEFLATED)
        
    # Delete all files after the zip action
    for i in glob.glob(inShapefile.replace(".shp",".*")):
        os.remove(i)
        
    zipobj.close()
        
    print "Zip Done !"
    
    return newZipFN

if __name__ == '__main__':
    shapefile_zipper(sys.argv[1])
