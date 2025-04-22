from src.coordinates import Coordinates
TEST_DATA_POS = [
    ("123 321", (123, 321)),
    ("1.12 3.21", (1.12, 3.21)),
    ("146.038588 -41.805062", (146.038588, -41.805062))
]

TEST_DATA_NEG = [
    "1"
    "a"
    ""
    "12.1"
    "Brno 1"
    "1 Brno"
]

def test_coord_match():
    for data in TEST_DATA_POS:
        coords = Coordinates.from_str(data[0])
        assert coords is not None, f"input: {data[0]}"
        assert (coords.lat, coords.lon) == data[1]

def test_coord_no_match():
    for data in TEST_DATA_NEG:
        assert Coordinates.from_str(data) is None, f"input: {data}"
