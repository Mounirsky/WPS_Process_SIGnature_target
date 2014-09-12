#!/bin/sh 

# $1 -> login,
# $2 -> password,
# $3 -> nom du shape zippé (.zip),
# $4 -> url_geoserver,
# $5 -> nom du Vect Out
# $6 -> nombre de classes pour spécifier le style
# $7 -> l'adress email
# $8, $9 -> Temps de calcule (sec, min)

# Référence : http://docs.geoserver.org/stable/en/user/rest/examples/curl.html

# Déposer le shapefile zippé sur le géoserver distant
curl -v -u $1:$2 -XPUT -H 'Content-type: application/zip' --data-binary @$3  $4/rest/workspaces/geouest/datastores/$5/file.shp

# Publier la couche déposé
curl -v -u $1:$2 -XPUT -H "Content-type: text/plain" -d "file:///home/data/geoserverwps_data_dir/data/geouest/$5/$5.shp" $4/rest/workspaces/geouest/datastores/$5/external.shp

# Appliquer le style qui dépond du nombre de classes ISO
curl -u $1:$2 -XPUT -H 'Content-type: text/xml' -d '<layer><defaultStyle><name>jussie_'$6'class</name><workspace>geouest</workspace></defaultStyle></layer>' $4/rest/layers/geouest:$5

# Envoi d'un e-mail avec la référence de la couche publiée (ref : http://documentation.mailgun.com/user_manual.html#sending-via-api)
curl -s --user 'api:key-3h8v3f-mj6-wx7kj1k2koy8mhzbposj9' \
    https://api.mailgun.net/v2/sandboxa82f4c39303b4533ac2e3888adfe73dc.mailgun.org/messages \
    -F from='Geouest <postmaster@sandboxa82f4c39303b4533ac2e3888adfe73dc.mailgun.org>' \
    -F to=$7\
    -F subject='Message de Geoxxx' \
    -F text='Le taitement et terminé et votre couche nomée "'$5'" a été publiée avec succé !

Visualisez dans un visualiseur avancé: http://geoxxx.agrocampus-ouest.fr/mapfishapp/?wmc=http://geoxxx.agrocampus-ouest.fr/wmc/GeOuest/'$5'.wmc

Visualisez dans un visualiseur mobile: http://geoxxx.agrocampus-ouest.fr/sviewer/?wmc=http://geoxxx.agrocampus-ouest.fr/wmc/GeOuest/'$5'.wmc

Télécharger le ShapeFile: '$4'/geouest/wfs?service=WFS&version=1.0.0&request=GetFeature&typename='$5'&outputFormat=SHAPE-ZIP

Télécharger le KML (Google Earth): '$4'/geouest/wms/kml?layers=geouest:'$5'

Le temps de traitement et de '$8' secondes ('$9' minutes).'
