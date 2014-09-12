#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 17:01:26 2014

@author: Mounir
"""

from pywps.Process.Process import WPSProcess
import time


start = time.time()

class Process(WPSProcess):
    def __init__(self):
        
        # initialisation process
        WPSProcess.__init__(self,
                            identifier="SIGnature_target_WPS",      
                            title="Detection de la Jussie aquatique sur le BV de La Vilaine",
                            version = "1.0", 
                            storeSupported = True,
                            statusSupported = True,
                            abstract="""Ce WPS permet de detecter la Jussie aquatique dans un bassain 
                            versant a partir des images stellites Spot5 et de ROI Jussie. 
                            le resultat sera l'envoi d'un e-mail contenant l'adresse du context
                            de la carte (Atlas) ainsi que le lien de téléchargement de la couche vecteur jussie.""")
                                          
        # Inputs
                                          
        # Complexe inputs                                
        # ROI en format GML (Optionel)                                        
        self.my_roi = self.addComplexInput(identifier = "ROI_Jussie",
                                            title = "Polygones de verite terrain Jussie",
                                            formats = [{'mimeType': 'text/xml'}],
                                            minOccurs = 0 )

#        self.zone_clip = self.addComplexInput(identifier = "Zone de clip",
#                                            title = "Couche vecteur due la zone a traiter",
#                                            formats = [{'mimeType': 'text/xml'}] )                                                 

        # WCS (si il y a une couche male publié sur l'adresse URL du geoserver le get_wcs ne marchra pas)

        self.url_wcs = self.addLiteralInput(identifier = "url_wcs",
                                            title = "L'adresse URL du serveur WCS",
                                            type = type(""),
                                            default="")
                                            
        self.namespace_wcs = self.addLiteralInput(identifier = "namespace_wcs",
                                            title = "Nom de l'image satellite sur le Geoserver",
                                            type = type(""),
                                            default="")

        # Literal Inputs
        self.url_wfs_RH = self.addLiteralInput(identifier = "url_wfs_RH",
                                            title = "L'adresse URL du serveur WFS",
                                            type = type(""),
                                            default="http://geoxxx.agrocampus-ouest.fr/geoserverwps/geouest")
                                            
        # Nome de la couche Reseau hydrographique sur le geoserver
        self.namespace_wfs_RH = self.addLiteralInput(identifier = "namespace_wfs_RH",
                                            title = "Nom de la couche vecteur Reseau hydrographique sur le Geoserver",
                                            type = type(""),
                                            default="geouest:RH_surfacique_BV_Vilaine")

                                            
        # L'angle spectral en degrés                            
        self.spectral_angle = self.addLiteralInput(identifier = "Angle spectral",
                                            title = "L' angle spectrale en degres pour la classification SAM",
                                            type = type(1.0),
                                            default=1.0)
                                  
        self.n_classes = self.addLiteralInput(identifier = "Nombre de classes",
                                            title = "Nombre de classes de la classification Cluster Analyses",
                                            type = type(2),
                                            allowedValues=[3,2],
                                            default=3)
                                            
        # Literal inputs (pour la publication de la couche résultat sur Geoserver)                                
        self.email = self.addLiteralInput(identifier = "E-Mail",
                                            title = "Entrer votre adresse email pour recevoir le resultat du traitement",
                                            type = type(""),
								    minOccurs = 0,
                                            default = "" )
                                            
        # Output

        self.text_out = self.addLiteralOutput(identifier="text_out",
                                         type = type(""),
                                         title = "A literal response output")

        self.url = self.addLiteralOutput(identifier="url",
                                         type = type(""),
                                         title = "URL de la couche en sortie")

        self.layer = self.addLiteralOutput(identifier="layer",
                                         type = type(""),
                                         title = "Nom de la couche en sortie")                                        

# Execution
        
    def execute(self):
        
        import os
        # création du suffixe au dépond de la date et l'heure de l'exucution, afin de nommer la couche en sortie
        suffix = time.strftime('%Y%m%d-%H%M%S',time.localtime())

        self.text_out.setValue(0)
        
        # Constantes internes
        url_wfs_ROI = "http://geoxxx.agrocampus-ouest.fr/geoserverwps/geouest"
        url_geoserver = "http://geoxxx.agrocampus-ouest.fr/geoserverwps"
        nomVectOut = "Jussie_"+suffix
        login = "gi2014"
        password = "gi20132014"
        workspace = "geouest"
        
        # Télécharger l'image en WCS
        self.cmd("./Apps_SIGnature_target/get_wcs.py %s %s" % (self.url_wcs.getValue(), 
                                                        self.namespace_wcs.getValue()))
        # Récupérer le chemain de l'image téléchargée
        Image_in = '/tmp/'+ self.namespace_wcs.getValue() +'.tif'         

        # Choisir le vecteur ROI correpondant à l'image WCS en entrée
        if self.namespace_wcs.getValue() == "geouest:spot_2012-30-09_up-l":
            Roi_name = "geouest:ROI_up-l"
            
        if self.namespace_wcs.getValue() == "geouest:spot_2012-30-09_dw-l":
            Roi_name = "geouest:ROI_dw-l"
            
        if self.namespace_wcs.getValue() == "geouest:spot_2012-09-09_up-r":
            Roi_name = "geouest:ROI_up-r"
            
        if self.namespace_wcs.getValue() == "geouest:spot_2012-09-09_dw-r":
            Roi_name = "geouest:ROI_dw-r"
            
        if self.namespace_wcs.getValue() == "geouest:Mosaic-Spot_2012":
            Roi_name = "geouest:ROI_dw-r"
   
        
        
        # Charger le vecteur ROI en WFS
        # si l'utilisateur à dessiner un ROI, celui-là va être utilisé           
        if self.my_roi.getValue() is not None:
            Roi_in = self.my_roi.getValue()
        # si non, le programe va utiliser l'ROI choisi au dépond de l'image
        else:
            self.cmd("./Apps_SIGnature_target/get_wfs.py %s %s" % (url_wfs_ROI, Roi_name))
            Roi_in = '/tmp/'+ Roi_name +'.gml'
        
        # Charger le vecteur réseau hydrographique en WFS
        self.cmd("./Apps_SIGnature_target/get_wfs.py %s %s" % (self.url_wfs_RH.getValue(), 
                                                        self.namespace_wfs_RH.getValue())) 
                                                        
        RH_in = '/tmp/'+ self.namespace_wfs_RH.getValue() +'.gml'
        
        # Lencement du traitement avec les couches récupérée par WCS et WFS
        self.cmd("./Apps_SIGnature_target/SIGnature_target_ows.sh %s %s %s %s %s %s" % (Image_in,
                                                                                      Roi_in,
                                                                                          RH_in,
                                                                                            self.spectral_angle.getValue(),
                                                                                                self.n_classes.getValue(),
                                                                                                    nomVectOut))



        
        # Recuperation du nom du vecteur en sortie
        shape_name = nomVectOut+".shp"
        
        # Zipper le vecteur en sortie du traitement et retourner le chemain du fichier zippé       
        self.cmd("./Apps_SIGnature_target/shapefile_zipper.py %s" % (shape_name))
        zippedshape = "/tmp/zip_"+ nomVectOut +".zip"
        
        # Récupérer le nombre de classes ISODATA pour l'utiliser comme référence dans le choix du style de la couche crée.
        style_class = str(self.n_classes.getValue())
        
        # Calcule du temps du traitement
        temps = int(time.time() - start)
        temps_sec = str(temps)
        temps_min = str(temps/60)
        
        # deposer, publier et appliquer un style du shpefile zippé au géoserver, puis envoyer un e-mail à l'utilisateur
        self.cmd("./Apps_SIGnature_target/shape_publisher.sh %s %s %s %s %s %s %s %s %s" % (login, 
                                                                                   password, 
                                                                                      zippedshape, 
                                                                                        url_geoserver, 
                                                                                            nomVectOut,
                                                                                                style_class,
                                                                                                    self.email.getValue(),
                                                                                                        temps_sec,
                                                                                                           temps_min))
                
        # Supprimer le fichier zippé
        os.remove(zippedshape)
        
        # Générer un fichier de context WMC avec la couche résultat
        self.cmd("./Apps_SIGnature_target/wmc_generator.py %s %s %s %s %s" % (nomVectOut, 
                                                                       style_class, 
                                                                           url_geoserver, 
                                                                               self.namespace_wcs.getValue(), 
                                                                                    self.url_wcs.getValue()))
        
        # Literal outputs
        # URL de la couche en sortie
        self.url.setValue(url_geoserver+"/"+workspace+"/wms")
        # Nom de la couche en sortie
        self.layer.setValue(nomVectOut)
        # Temps de traitement
        self.text_out.setValue("Veuillez vérifiez votre e-mail ! \n Temps(s): "+temps_sec+" sec, ( "+temps_min+" min)")
        
        return