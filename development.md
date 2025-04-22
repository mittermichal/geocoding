# Development

## setup

`docker-compose -f docker-compose.local.yml up`

`cd data && curl -O https://download.geofabrik.de/europe/czech-republic-latest.osm.pbf && cd ..`

`docker run -v $(pwd)/data:/data --network="host" iboates/osm2pgsql -c -d o2p -U o2p -H localhost -O flex -S /data/addresses.lua /data/czech-republic-latest.osm.pbf`

`pip install -r requirements`

`source .venv/bin/activate`

`fastapi dev src/main.py`


## psql:
`docker compose -f docker-compose.local.yml exec postgis psql -U o2p`

## libpostal:
```py
import zerorpc
c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
c.parse("Brno, CZ")
c.expand("Brno, CZ")
c.expandAndParse("Brno, CZ")
```

## Unit tests:
```bash
PYTHONPATH=. pytest
```

