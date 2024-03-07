from typing import NamedTuple


class BoundingBox(NamedTuple):
    west: float
    south: float
    east: float
    north: float

    def as_list(self) -> list[float]:
        return list(self)
