#!/bin/sh 

date
START=$(date +%s)

# Importer l'image Tiff en WCS sauvgarder sur le Geoserver et  la convertir en format inter de SAGA -sgrd-
saga_cmd -f=q libio_gdal "GDAL: Import Raster" -FILES=$1 -GRIDS=image_in

# Ajout au nom des fichiers vecteurs (gml) généré par pyWps un ".gml" pour que la fonction ogr2ogr les reconait comme "GML"

mv $2 $2.gml
mv $3 $3.gml

# Convertion du fichier GML en Shape
ogr2ogr -f "ESRI Shapefile" roi.shp $2.gml
ogr2ogr -f "ESRI Shapefile" zone.shp $3.gml

# Découpage de l'image (4 bands) en entrée avec le vecteur de la zone a traité (RH)
saga_cmd -f=q libshapes_grid "Clip Grid with Polygon" -OUTPUT=Clip_image -INPUT="image_in_0001.sgrd;image_in_0002.sgrd;image_in_0003.sgrd;image_in_0004.sgrd" -POLYGONS=zone.shp

# Classification supervisée SAM de le la zone d'intéret de l'image sat (découpée)
saga_cmd -f=q libimagery_classification "Supervised Classification" -GRIDS="Clip_image_0001.sgrd;Clip_image_0002.sgrd;Clip_image_0003.sgrd;Clip_image_0004.sgrd" -ROI=roi.shp -ROI_ID=1 -CLASS_INFO=NULL -CLASSES=Classif_SAM -QUALITY=NULL -METHOD=4 -NORMALISE -RELATIVE_PROB=0 -THRESHOLD_ANGLE=$4

# Création d'une couche vecteur à partire de la classe du SAM voulue
saga_cmd -f=q libshapes_grid "Vectorising Grid Classes" -GRID=Classif_SAM.sgrd -POLYGONS=Vecteur_SAM -CLASS_ALL=0 -CLASS_ID=1.0 -SPLIT=0

# Découpage de l'image (4 bands) zonne d'intéret avec le vecteur créé à partire de la classification SAM
saga_cmd -f=q libshapes_grid "Clip Grid with Polygon" -OUTPUT=Clip_sam -INPUT="Clip_image_0001.sgrd;Clip_image_0002.sgrd;Clip_image_0003.sgrd;Clip_image_0004.sgrd" -POLYGONS=Vecteur_SAM.shp

# Classification non-supervisée Cluster Analysise de le la zone découpée l'image sat
saga_cmd -f=q libimagery_classification "Cluster Analysis for Grids" -GRIDS="Clip_sam_0001.sgrd;Clip_sam_0002.sgrd;Clip_sam_0003.sgrd;Clip_sam_0004.sgrd" -CLUSTER=Classif_clusters -STATISTICS=NULL -METHOD=2 -NCLUSTER=$5

# Création d'une couche vecteur à partire de la ou les classes voulue
saga_cmd -f=q libshapes_grid "Vectorising Grid Classes" -GRID=Classif_clusters.sgrd -POLYGONS=/home/tmp/$6 -CLASS_ALL=1 -CLASS_ID=0 -SPLIT=0

#mv $6 $6.shp

# Convertion du fichier vecteur shape de sortie en "GML" (pour qu'il puise s'afficher dans le clien Qgis)
#ogr2ogr -f "GML" $6 $6.shp

# Calcule du temps du traitement
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Le temps de traitement est de $DIFF secondes"

# Supprimer les fichier téléchargés pas la requete WCS & WFS
#rm $1
#rm $2.gml
#rm $2.gfs
#rm $3.gml
#rm $3.gfs
