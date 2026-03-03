"""Fake database for unit testing."""


class FakeDatabase:
    """Minimal in-memory database for unit testing.

    Implements the same interface as :class:`permaculture.database.Database`
    but operates entirely in memory, making it suitable for fast,
    isolated unit tests.
    """

    def __init__(self, plants):
        self._plants = plants

    def search(self, query, score=0.6):
        """Substring search on scientific and common names."""
        for plant in self._plants:
            sci_name = plant.get("scientific name", "")
            common_names = [
                k.split("/", 1)[1]
                for k, v in plant.items()
                if k.startswith("common name/") and v is True
            ]
            if query.lower() in sci_name.lower() or any(
                query.lower() in cn.lower() for cn in common_names
            ):
                yield {
                    "scientific_name": sci_name,
                    "common_names": common_names,
                }

    def lookup(self, names, score=1.0):
        """Yield plants matching the given scientific names."""
        for plant in self._plants:
            if plant.get("scientific name") in names:
                yield plant
