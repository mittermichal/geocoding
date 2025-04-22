import dataclasses
import re
from typing import Self


@dataclasses.dataclass
class Coordinates:
    lon: float
    lat: float

    @classmethod
    def from_str(cls, q:str) -> Self | None:
        try:
            lat, lon = re.split(r'\s+|,\s+|\s+,\s+|,', q)

            return cls(lon=float(lon), lat=float(lat))
        except ValueError:
            return None

# COORD_PATTERN = r'(\d+(\.\d+)?) (\d+)'
# coord_prog: re.Pattern[AnyStr] = re.compile(COORD_PATTERN) # it should be cached anyway, see: https://docs.python.org/3/library/re.html#re.compile
# coord_prog.match(q)