# Research:

## Geocoding wiki https://en.wikipedia.org/wiki/Address_geocoding
### relative input:
"Across the street from the Empire State Building." The location being sought cannot be determined without identifying the Empire State Building. Geocoding platforms often do not support such relative locations, but advances are being made in this direction.
I guess too complicated to do in a day, but could be discussed,
### absolute input 
- adress/name -> (lon,lat)

### Processing
- import only useful data - address,name,...

### Geocoding algo.
- Direct match
- Interpolated match
  - only needed if reference dataset is missing house numbers? 
  - check coverage of OSM data? 
  - could official parcel dataset improve it?


## Paper: tidygeocoder: An R package for geocoding https://joss.theoj.org/papers/10.21105/joss.03544.pdf
- overviews of geocoding
- describes different available API, how they differ
- doesn't actually implement it

## Paper: some OSM data evaluation: https://onlinelibrary.wiley.com/doi/full/10.1111/tgis.13089
- reverse geocoding from OSM might be innacurate in conclusion

## Paper: Geocoding Best Practices: Review of Eight Commonly Used Geocoding Systems
- https://spatial.usc.edu/wp-content/uploads/2014/03/gislabtr10.pdf
- nice diagram of geocoding workflow - (Figure 2)

## Paper: Geocoding Best Practices: Reference Data, Input Data and Feature Matching
- https://spatial.usc.edu/wp-content/uploads/2014/03/gislabtr8.pdf

## https://www.mapzen.com/blog/inside-libpostal/

## Geocoding project https://github.com/dunkelstern/osmgeocoder
- PostGIS
- import times of Europe region counted in hours
- imposm3
- reverse - 1st tries OSM if no results then search in openstreetadress.io
- limit param in forward and reverse
- 

## https://github.com/osm-search/Nominatim/blob/master/vagrant/Install-on-Ubuntu-22.sh
- even OSM Nominatim uses PostGIS
- using osm2pgsql

# Pelias.io
- has multiple open data sources (Polylines)
- libpostal
- Elasticsearch

## OSM import
- imposm3 - go, has "Automatic OSM updates, "Alternatives: Osm2pgsql – database import tool written in C++ with similar or better performance and ability to customize database layout"
- osm2pgsql - C++
- https://ninefinity.org/post/importing-openstreetmap-planet-osm-with-imposm3-and-osmosis/ 2016
- features: https://imposm.org/docs/imposm3/latest/#features vs https://osm2pgsql.org/about/features/

## Libpostal https://github.com/openvenues/libpostal
- has simple py wrapper
```
>>>start=time.time();parse_address('Tišnovská 137 614 00 Brno CZ');print(time.time()-start);
[('tišnovská', 'road'), ('137', 'house_number'), ('614 00', 'postcode'), ('brno', 'city'), ('cz', 'country')]
0.0003941059112548828
```
- by default 2GB memory
- I assume that I can then map this to addr:* OSM tags - WHERE addr:city='Brno' and addr:road
- maybe order where keys from the biggest area to smallest
- don't understand why:
```
expand_address('Erbenova 1, Prague, CZ', languages='cz')
['erbenova 1 prague cz']
```
- image "pasupulaphani/libpostal-zeromq" - outdated?, has expandAndParse



# Random
- https://www.postgresql.org/docs/current/gin.html
- do only decimal lon lat geocoding, consider how to do DMS(degree+minutes+seconds) in discussion
- web server on same image as postgis?
- localization (e.g. Prague/Praha)
- https://github.com/ultrasamad/postgis-cheatsheet
- https://stackoverflow.com/questions/63270196/how-to-do-persistent-database-connection-in-fastapi
- https://github.com/akadouri/osm2pgsql-docker-quickstart
- https://gist.github.com/jpetazzo/5177554

##  Brno wiki coords
- DMS:     49° 11′ 33″ N, 16° 36′ 30″ E
- Decimal: 49.1925, 16.608333

## Projections
- EPSG:3857 -> mercator
- EPSG:4326 -> wsg84 lat,long

## Cze PBF
```bash
cd data
`curl -O https://download.geofabrik.de/europe/czech-republic-latest.osm.pbf`
```

## Luxemburg PBF
- only 100MB
```bash
cd data
curl -O https://download.geofabrik.de/europe/czech-republic-latest.osm.pbf
https://osm.kewl.lu/luxembourg.osm/
```

## Andorra PBF
- https://download.geofabrik.de/europe/andorra-latest.osm.pbf
- only 3MB

## DB structure for geocoding
- maybe don't need non-point geometry (Line (street), Polygon (city, area,...), ...) for geocoding, just its center - https://postgis.net/docs/ST_Centroid.html or better ST_PointOnSurface , create geom index on this for search
- https://wiki.openstreetmap.org/wiki/Tag%3aboundary=administrative
- https://wiki.openstreetmap.org/wiki/Key:admin_level "A data consumer looking for municipalities corresponding to "city", "town" or "village" boundaries will find these tagged anywhere from admin_level=4 (e.g. relation Berlin) to admin_level=10 (e.g. relation Cheddar, UK)."
- https://nominatim.org/release-docs/develop/develop/Database-Layout/
- https://postgis.net/workshops/postgis-intro/indexing.html