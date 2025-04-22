# Minimal Geocoding API Service

## Setup with Docker:
- clone the repo.
- run the services:
```bash
docker-compose up --build
````
- Import data:
```bash
docker run -v $(pwd)/data:/data --network=geocoding_postgis iboates/osm2pgsql -c -d o2p -U o2p -H postgis -O flex -S /data/addresses.lua https://download.geofabrik.de/europe/andorra-latest.osm.pbf
```
- for cz use: https://download.geofabrik.de/europe/czech-republic-latest.osm.pbf
- swagger UI will be available at http://localhost:8000/docs

### Request examples:
```bash
# Andorra
curl --get --data-urlencode 'q=42.513051, 1.539376' --data-urlencode 'limit=3' localhost:8000
curl --get --data-urlencode 'q=Carrer Ramón Armengol 2' --data-urlencode 'limit=10' localhost:8000

# CZ
curl --get --data-urlencode 'q=49.212595, 16.626566' --data-urlencode 'limit=3' localhost:8000
curl --get --data-urlencode 'q=Tišnovská 1505/137' --data-urlencode 'limit=10' localhost:8000
```

### Inspecting postgis:
```bash
docker compose exec postgis psql -h 127.0.0.1 -p 5432 -d o2p -U o2p
```

## Architecture:
services: FastAPI backend, PostGIS, libpostal
service inter-communication:
  - FastAPI - asyncpg - PostGIS
  - FastAPI - ZeroMQ(zerorpc) - libpostal
- importing OSM data with osm2pgsql with Lua defined style

## Architecture explanation:
- web service:
  - python FastAPI for familiarity
  - async - Searching in the database should be just I/O given there is proper indexing, only little logic in python, so it should be able to handle many requests.
- PostGIS - familiarity, used by other geocoding projects
- libpostal - claims to parse and label address data with high accuracy, used by other geocoding projects, fast. Separate service because of memory usage and init time. Chosen ZeroMQ wrapped docker image for speed, and ease to use, though it might be outdated.
- osm2pgsql - support flexible customization of import with Lua, rather than YAML configuration of imposm3

## Possible improvements or scalability discussion:

- import relations with boundary=administrative and name tags from OSM
  - to add:
    - expand `addrs` record for reverse geocoding if city/state/country missing during import
    - query only addresses within their boundary for forward geocoding if query has some administrative area
  - ref: https://github.com/osm2pgsql-dev/osm2pgsql/blob/master/flex-config/route-relations.lua
- import roads: ways with highway=* and name tags from OSM
  - for places with missing house numbers for reverse geocoding

- handling variations of address of same place - add supporting table with language or other variations that point back to `addrs` record
  - consider doing full text search over expanded address (pg_trgm)
- handle incremental updates from OSM
- limit reverse geocoding to some reasonable distance
- run test on some large geocoding test data


### More datasources
- OpenAddresses, WhosOnFirst, geonames ... but how to handle duplicates?
- need to have good understanding of differences between them and OSM

### Scalability

- can replicate PostGIS DB with already imported tables
- libpostal probably needs to be replicated much less than backend (fast, but 2GB memory use)
- not sure if partitioning data by area is good idea

#### Sessions on client
- client requests a session to some kind of session handler service that would assign unique session (could be used for typing monitoring).
- if service is supposed to be global then session service could assign to different server location to improve latency (e.g. 300ms ping between Tokyo-EU) based on either geoip db or just pinging those servers from client.

#### Move some computation to client
- check if query is for reverse geocoding on client, only some logic without much data is needed
- usually user is browsing map and view coordinates could be added to query to sort the results by distance

### Libpostal
- will normalize address query "into one or more normalized forms suitable for geocoder queries"
- make Libpostal optional for development and testing of mapping between its output and database, or expose such service for it
- investigate if parsing does some other changes than lowercase transform that could lead to search miss
- how could be its "expand" function used in geocoding?

### Improve reverse geocoding format
- https://github.com/OpenCageData/address-formatting
