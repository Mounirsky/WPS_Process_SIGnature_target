# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 00:37:32 2014

@author: Mounirsky
"""

#================================================================================================
# Cette application permet de générer un fichier (.wmc) depuis un ficher de cotexte (WCS) de base
# les changements déponderants de la chouche créé par le wps :
# sys.argv[1] : nom de la couche créé	
# sys.argv[2] : Nombre de classes ISODATA
# sys.argv[3] : URL du geoserver où la couche à été publiée
# sys.argv[4] : Nom de l'image traitée
# sys.argv[5] : URL de l'image traitée
#================================================================================================

import sys
from owslib.wms import WebMapService

print "Strat generating WMC"p

# Récupération de la bonding-box et EPSG de la couche en sortie
wms = WebMapService(sys.argv[3] + "/geouest/wms/", version='1.1.1')
bboxx = wms[sys.argv[1]].boundingBox

# Modification du contenu du fichier WMC de base avec une concetination (doc string)
wmc_file = """<?xml version="1.0" encoding="UTF-8"?>
<ViewContext xmlns="http://www.opengis.net/context" version="1.1.0" id="b78393a1f8c27" xsi:schemaLocation="http://www.opengis.net/context http://schemas.opengis.net/context/1.1.0/context.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <General>
        """+'<Window width="1613" height="980"/><BoundingBox minx="'+str(bboxx[0])+'" miny="'+str(bboxx[1])+'" maxx="'+str(bboxx[2])+'" maxy="'+str(bboxx[3])+'" SRS="'+bboxx[4]+'"/>'+"""
        """+"<Title>Alertes de Jussie aquatique (Image "+ sys.argv[4] +")</Title>"+"""
        <Extension>
            <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-1878330.58618499991" miny="4870726.52893589996" maxx="3306658.96357630007" maxy="8984724.28838369995"/>
        </Extension>
    </General>
    <LayerList>

        <Layer queryable="0" hidden="1">
            <Server service="OGC:WMS" version="1.1.1">
                <OnlineResource xlink:type="simple" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="http://osm.geobretagne.fr/gwc01/service/wms"/>
            </Server>
            <Name>osm:google</Name><Title>OpenStreetMap</Title><Abstract>carte OpenStreetMap licence CreativeCommon by-SA</Abstract>
            <MetadataURL>
                <OnlineResource xlink:type="simple" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="http://wiki.openstreetmap.org/wiki/FR:OpenStreetMap_License"/>
            </MetadataURL>
            <sld:MinScaleDenominator xmlns:sld="http://www.opengis.net/sld">266.5911979812229</sld:MinScaleDenominator><sld:MaxScaleDenominator xmlns:sld="http://www.opengis.net/sld">559082264.0287179</sld:MaxScaleDenominator>
            <FormatList>
                <Format current="1">image/png</Format>
            </FormatList>
            <StyleList>
                <Style>
                    <Name/><Title/>
                </Style>
            </StyleList>
            <Extension>
                <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-1878330.58618499991" miny="4870726.52893589996" maxx="3306658.96357630007" maxy="8984724.28838369995"/><ol:tileSize xmlns:ol="http://openlayers.org/context" width="256" height="256"/>
                <ol:numZoomLevels xmlns:ol="http://openlayers.org/context">100</ol:numZoomLevels><ol:units xmlns:ol="http://openlayers.org/context">m</ol:units><ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer><ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher><ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile><ol:transitionEffect xmlns:ol="http://openlayers.org/context">resize</ol:transitionEffect>
            </Extension>
        </Layer>

	<Layer queryable="0" hidden="1">
            <Server service="OGC:WMS" version="1.1.1">
                <OnlineResource xlink:type="simple" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="http://tile.geobretagne.fr/gwc02/service/wms"/>
            </Server>
            <Name>carte</Name><Title>Cartes IGN</Title>
            <MetadataURL>
                <OnlineResource xlink:type="simple" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="http://www.ign.fr/"/>
            </MetadataURL>
            <FormatList>
                <Format current="1">image/jpeg</Format>
            </FormatList>
            <StyleList>
                <Style>
                    <Name/><Title/>
                </Style>
            </StyleList>
            <Extension>
                <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-1878330.58618499991" miny="4870726.52893589996" maxx="3306658.96357630007" maxy="8984724.28838369995"/><ol:tileSize xmlns:ol="http://openlayers.org/context" width="256" height="256"/>
                <ol:numZoomLevels xmlns:ol="http://openlayers.org/context">17</ol:numZoomLevels><ol:units xmlns:ol="http://openlayers.org/context">m</ol:units><ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer><ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher><ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile>
            </Extension>
        </Layer>
        
	<Layer queryable="0" hidden="0">
            <Server service="OGC:WMS" version="1.1.1">
                <OnlineResource xlink:type="simple" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="http://tile.geobretagne.fr/gwc02/service/wms"/>
            </Server>
            <Name>satellite</Name><Title>Orthophotographie IGN</Title>
            <MetadataURL>
                <OnlineResource xlink:type="simple" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="http://www.ign.fr/"/>
            </MetadataURL>
            <FormatList>
                <Format current="1">image/jpeg</Format>
            </FormatList>
            <StyleList>
                <Style>
                    <Name/><Title/>
                </Style>
            </StyleList>
            <Extension>
                <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-1878330.58618499991" miny="4870726.52893589996" maxx="3306658.96357630007" maxy="8984724.28838369995"/><ol:tileSize xmlns:ol="http://openlayers.org/context" width="256" height="256"/>
                <ol:numZoomLevels xmlns:ol="http://openlayers.org/context">17</ol:numZoomLevels><ol:units xmlns:ol="http://openlayers.org/context">m</ol:units><ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer><ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher><ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile>
            </Extension>
        </Layer>

	<Layer queryable="1" hidden="1">
         <Server service="OGC:WMS" version="1.3.0">
            """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ sys.argv[5] +'/ows?SERVICE=WMS&amp;" />'+"""
         </Server>
         """+'<Name>'+ sys.argv[4] +'</Name><Title>'+ sys.argv[4] +'</Title>'+"""
         <sld:MinScaleDenominator xmlns:sld="http://www.opengis.net/sld">266.5911979812229</sld:MinScaleDenominator>
         <sld:MaxScaleDenominator xmlns:sld="http://www.opengis.net/sld">559082264.0287179</sld:MaxScaleDenominator>
         <FormatList>
            <Format current="1">image/png</Format>
            <Format>application/atom+xml</Format>
            <Format>application/pdf</Format>
            <Format>application/vnd.google-earth.kml+xml</Format>
            <Format>application/vnd.google-earth.kml+xml;mode=networklink</Format>
            <Format>application/vnd.google-earth.kmz</Format>
            <Format>image/geotiff</Format>
            <Format>image/geotiff8</Format>
            <Format>image/gif</Format>
            <Format>image/jpeg</Format>
            <Format>image/png; mode=8bit</Format>
            <Format>image/svg+xml</Format>
            <Format>image/tiff</Format>
            <Format>image/tiff8</Format>
         </FormatList>
         <StyleList>
            <Style>
               <Name>raster_false_color</Name>
               <Title />
               <LegendURL width="20" height="20" format="image/png">
                  """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ sys.argv[5] +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ sys.argv[4] +'" />'+"""
               </LegendURL>
            </Style>
            <Style>
               <Name>raster_true_colors</Name>
               <Title />
               <LegendURL width="20" height="20" format="image/png">
                  """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ sys.argv[5] +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ sys.argv[4] +'&amp;style=raster_true_colors" />'+"""
               </LegendURL>
            </Style>
            <Style>
               <Name>raster</Name>
               <Title>Default Raster</Title>
               <Abstract>A sample style that draws a raster, good for displaying imagery</Abstract>
               <LegendURL width="20" height="20" format="image/png">
                  """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ sys.argv[5] +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ sys.argv[4] +'&amp;style=raster" />'+"""
               </LegendURL>
            </Style>
         </StyleList>
         <Extension>
            <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-1878330.58618499991" miny="4870726.52893589996" maxx="3306658.96357630007" maxy="8984724.28838369995" />
            <ol:tileSize xmlns:ol="http://openlayers.org/context" width="512" height="512" />
            <ol:transparent xmlns:ol="http://openlayers.org/context">true</ol:transparent>
            <ol:numZoomLevels xmlns:ol="http://openlayers.org/context">22</ol:numZoomLevels>
            <ol:units xmlns:ol="http://openlayers.org/context">m</ol:units>
            <ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer>
            <ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher>
            <ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile>
            <ol:transitionEffect xmlns:ol="http://openlayers.org/context">map-resize</ol:transitionEffect>
            <ol:gutter xmlns:ol="http://openlayers.org/context">10</ol:gutter>
         </Extension>
      </Layer>

        <Layer queryable="1" hidden="0">
            <Server service="OGC:WMS" version="1.3.0">
                <OnlineResource xlink:type="simple" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="http://geoxxx.agrocampus-ouest.fr/geoserverwps/ows?SERVICE=WMS&amp;"/>
            </Server>
            """+'<Name>'+ sys.argv[1] +'</Name><Title>'+ sys.argv[1] +'</Title>'+"""
	    <sld:MinScaleDenominator xmlns:sld="http://www.opengis.net/sld">266.5911979812229</sld:MinScaleDenominator>
	    <sld:MaxScaleDenominator xmlns:sld="http://www.opengis.net/sld">559082264.0287179</sld:MaxScaleDenominator>
            <FormatList>
                <Format current="1">image/png</Format><Format>application/atom+xml</Format><Format>application/pdf</Format><Format>application/vnd.google-earth.kml+xml</Format><Format>application/vnd.google-earth.kml+xml;mode=networklink</Format><Format>application/vnd.google-earth.kmz</Format><Format>image/geotiff</Format><Format>image/geotiff8</Format><Format>image/gif</Format><Format>image/jpeg</Format><Format>image/png; mode=8bit</Format><Format>image/svg+xml</Format><Format>image/tiff</Format><Format>image/tiff8</Format>
            </FormatList>
            <StyleList>
                <Style>
                    """+'<Name>jussie_'+ sys.argv[2] +'class</Name><Title/>'+"""
                    <LegendURL width="20" height="20" format="image/png">
                        """+'<OnlineResource xlink:type="simple" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="'+ sys.argv[3] +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ sys.argv[1] +'"/>'+"""
                    </LegendURL>
                </Style>
            </StyleList>
            <Extension>
                <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-1878330.58618499991" miny="4870726.52893589996" maxx="3306658.96357630007" maxy="8984724.28838369995"/><ol:tileSize xmlns:ol="http://openlayers.org/context" width="512" height="512"/>
                <ol:transparent xmlns:ol="http://openlayers.org/context">true</ol:transparent><ol:numZoomLevels xmlns:ol="http://openlayers.org/context">22</ol:numZoomLevels><ol:units xmlns:ol="http://openlayers.org/context">m</ol:units><ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer><ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher><ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile><ol:transitionEffect xmlns:ol="http://openlayers.org/context">map-resize</ol:transitionEffect><ol:gutter xmlns:ol="http://openlayers.org/context">10</ol:gutter>
            </Extension>
        </Layer>

	<Layer queryable="1" hidden="0">
	      <Server service="OGC:WMS" version="1.3.0">
		 <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://geoxxx.agrocampus-ouest.fr/geoserverwps/geouest/ows?SERVICE=WMS&amp;" />
	      </Server>
	      <Name>Contour_bv</Name>
	      <Title>Contour_bv</Title>
	      <sld:MinScaleDenominator xmlns:sld="http://www.opengis.net/sld">266.5911979812229</sld:MinScaleDenominator>
	      <sld:MaxScaleDenominator xmlns:sld="http://www.opengis.net/sld">559082264.0287179</sld:MaxScaleDenominator>
	      <FormatList>
		 <Format current="1">image/png</Format>
		 <Format>application/atom+xml</Format>
		 <Format>application/pdf</Format>
		 <Format>application/vnd.google-earth.kml+xml</Format>
		 <Format>application/vnd.google-earth.kml+xml;mode=networklink</Format>
		 <Format>application/vnd.google-earth.kmz</Format>
		 <Format>image/geotiff</Format>
		 <Format>image/geotiff8</Format>
		 <Format>image/gif</Format>
		 <Format>image/jpeg</Format>
		 <Format>image/png; mode=8bit</Format>
		 <Format>image/svg+xml</Format>
		 <Format>image/tiff</Format>
		 <Format>image/tiff8</Format>
	      </FormatList>
	      <StyleList>
		 <Style current="1">
		    <Name>BV</Name>
		    <Title />
		    <LegendURL width="20" height="20" format="image/png">
		       <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://geoxxx.agrocampus-ouest.fr/geoserverwps/geouest/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer=Contour_bv" />
		    </LegendURL>
		 </Style>
		 <Style>
		    <Name>polygon</Name>
		    <Title>Default Polygon</Title>
		    <Abstract>A sample style that draws a polygon</Abstract>
		    <LegendURL width="20" height="20" format="image/png">
		       <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://geoxxx.agrocampus-ouest.fr/geoserverwps/geouest/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer=Contour_bv&amp;style=polygon" />
		    </LegendURL>
		 </Style>
	      </StyleList>
	      <Extension>
		 <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-1878330.58618499991" miny="4870726.52893589996" maxx="3306658.96357630007" maxy="8984724.28838369995" />
		 <ol:tileSize xmlns:ol="http://openlayers.org/context" width="512" height="512" />
		 <ol:transparent xmlns:ol="http://openlayers.org/context">true</ol:transparent>
		 <ol:numZoomLevels xmlns:ol="http://openlayers.org/context">22</ol:numZoomLevels>
		 <ol:units xmlns:ol="http://openlayers.org/context">m</ol:units>
		 <ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer>
		 <ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher>
		 <ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile>
		 <ol:transitionEffect xmlns:ol="http://openlayers.org/context">map-resize</ol:transitionEffect>
		 <ol:gutter xmlns:ol="http://openlayers.org/context">10</ol:gutter>
	      </Extension>
	</Layer>
    </LayerList>
</ViewContext>"""

print 'Changes are :'
print sys.argv[1]
print sys.argv[2]
print sys.argv[3]
print sys.argv[4]
print sys.argv[5]

with open(r'/var/www/georchestra/htdocs/wmc/GeOuest/'+ sys.argv[1] +'.wmc', "w") as f:
    f.write(wmc_file)

print "Done"