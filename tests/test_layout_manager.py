"""LayoutManager JSON yapılandırmasının geçerlilik testleri."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_layout_config_structure():
    with open(ROOT / "data" / "json" / "layout_config.json", encoding="utf-8") as f:
        config = json.load(f)
    assert isinstance(config, dict) or isinstance(config, list)


def test_extensions_json_entries_have_required_fields():
    with open(ROOT / "data" / "json" / "extensions.json", encoding="utf-8") as f:
        extensions = json.load(f)
    items = extensions.values() if isinstance(extensions, dict) else extensions
    for item in items:
        if isinstance(item, dict):
            assert "uuid" in item or "name" in item, f"uuid/name eksik: {item}"
