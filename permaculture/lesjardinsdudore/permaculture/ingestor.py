"""JSON file ingestor for testing."""

import json
import logging
import os
from pathlib import Path

from attrs import define

from permaculture.database import DatabasePlant

logger = logging.getLogger(__name__)


@define(frozen=True)
class JSONIngestor:
    """Ingest plants from JSON_INGESTOR_PATH."""

    path: Path | None

    @classmethod
    def from_config(cls, config):
        """Create a JSONIngestor from permaculture config."""
        path = os.environ.get("JSON_INGESTOR_PATH")
        return cls(Path(path) if path else None)

    def fetch_all(self):
        """Yield all plants from the JSON fixture file."""
        if self.path is None:
            logger.debug("json: JSON_INGESTOR_PATH not set, skipping")
            return

        data = json.loads(self.path.read_text())
        for plant in data:
            yield DatabasePlant(plant)

        logger.info("json: ingested %d plants", len(data))
