"""data/ altındaki JSON, UI ve şema dosyalarının bütünlük testleri."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def json_files():
    return sorted((DATA / "json").glob("*.json"))


@pytest.mark.parametrize("path", json_files(), ids=lambda p: p.name)
def test_json_is_valid(path):
    with open(path, encoding="utf-8") as f:
        json.load(f)  # geçersiz JSON'da exception fırlatır


@pytest.mark.parametrize("path", sorted((DATA / "ui").rglob("*.ui")), ids=lambda p: p.name)
def test_ui_files_are_valid_xml(path):
    ET.parse(path)


def test_gschema_is_valid_xml_and_uses_parslinux_id():
    schema = DATA / "schemas" / "org.parslinux.parslinux-gnome-greeter.gschema.xml"
    tree = ET.parse(schema)
    root = tree.getroot()
    assert root.tag == "schemalist"
    ids = [s.get("id") for s in root.findall("schema")]
    assert "org.parslinux.parslinux-gnome-greeter" in ids
    assert not any("pardus" in i.lower() for i in ids)


def test_gresource_paths_exist():
    """gresource.xml içinde tanımlı her yol data/ altında gerçekten olmalı."""
    res = ROOT / "parslinux-gnome-greeter.gresource.xml"
    tree = ET.parse(res)
    for file_el in tree.getroot().findall("gresource/file"):
        rel = file_el.text.strip()
        assert (DATA / rel).exists(), f"gresource'ta tanımlı ama dosya yok: {rel}"


def test_no_pardus_references_in_tracked_text_files():
    """Marka temizliği regresyon koruması: kod dosyalarında 'pardus' kalmamalı."""
    text_suffixes = {".py", ".json", ".ui", ".xml", ".in", ".build", ".po", ".pot"}
    own_test = Path(__file__).resolve()
    # Dokümantasyon dosyaları marka geçişini anlatmak için eski adı anabilir;
    # yalnızca kaynak/derleme dosyaları denetlenir.
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.resolve() == own_test:  # bu test dosyası anahtar kelimeyi içerir
            continue
        if path.name == "changelog":  # tarihsel paket kaydı — değiştirilmez
            continue
        if path.suffix not in text_suffixes and path.name not in {"control", "copyright", "rules"}:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "pardus" in content.lower():
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == [], "'pardus' geçen dosyalar: " + ", ".join(offenders)
