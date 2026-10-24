"""Use the crawler's exact approved copy exceptions in the hygiene scan."""
import importlib.util
from pathlib import Path


_path = Path(__file__).resolve().parents[1] / "scripts" / "crawl-check.py"
_spec = importlib.util.spec_from_file_location("acg_crawl_metadata", _path)
_crawler = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_crawler)


def description_over_limit(path: str, description: str) -> bool:
    return len(description) > _crawler.DESC_MAX and not _crawler.held_long_description_matches(path, description)
