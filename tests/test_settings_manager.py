"""SettingsManager birim testleri (saf Python mantığı)."""

import importlib.util
import sys
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parent.parent / "src" / "parslinux_gnome_greeter" / "managers" / "settings.py"


def _load_settings_module():
    """settings.py'yi paket zinciri (gi/pydbus) tetiklemeden izole yükler."""
    spec = importlib.util.spec_from_file_location("_pgg_settings", _SRC)
    module = importlib.util.module_from_spec(spec)
    # modülü önce sys.modules'a kaydet; böylece exec sırasında Gio/GSettings
    # kullanan modül düzeyi kod, conftest'teki sahte gi nesneleriyle çalışır
    # ve fixture'lardan sonra da erişilebilir kalır.
    sys.modules["_pgg_settings"] = module
    spec.loader.exec_module(module)
    return module


SettingsManager = _load_settings_module().SettingsManager


class FakeSettings:
    """Gio.Settings yerine geçen minimal sahte sınıf."""

    class Variant:
        """GLib.Variant benzeri; type_string + value ile de tek değerle de kurulabilir."""

        def __init__(self, type_string_or_value, value=None):
            self.value = value if value is not None else type_string_or_value

        def copy(self):
            return FakeSettings.Variant(self.value)

        @staticmethod
        def new(type_string, value):
            # GLib.Variant(type_string, value) kalıbını destekle
            return FakeSettings.Variant(value)

        def unpack(self):
            return self.value

        def get_type_string(self):
            v = self.value
            if isinstance(v, bool):
                return "b"
            if isinstance(v, int):
                return "i"
            if isinstance(v, str):
                return "s"
            if isinstance(v, list):
                return "as"
            return "v"

    def __init__(self, initial=None):
        self._data = dict(initial or {})

    def get_value(self, key):
        return self.Variant(self._data[key])

    def set_value(self, key, variant):
        self._data[key] = variant.value
        return True

    def get_strv(self, key):
        return list(self._data[key])

    def set_strv(self, key, value):
        self._data[key] = list(value)
        return True


@pytest.fixture
def manager(monkeypatch):
    fake = FakeSettings({
        "theme": "dark",
        "enabled": True,
        "count": 3,
        "wallpapers": ["/a.png", "/b.png"],
    })
    import _pgg_settings  # izole yüklenen modül sys.modules'ta olmalı
    manager = SettingsManager.__new__(SettingsManager)  # __init__ Gio'ya dokunmaz
    manager.settings = fake
    # GLib.Variant yerine FakeSettings.Variant kullan (gi sahte olabilir)
    monkeypatch.setattr(_pgg_settings, "GLib", FakeSettings, raising=False)
    return manager


def test_get_returns_unpacked_value(manager):
    assert manager.get("theme") == "dark"
    assert manager.get("enabled") is True
    assert manager.get("count") == 3


def test_set_writes_back(manager):
    manager.set("theme", "light")
    assert manager.get("theme") == "light"


def test_get_strv_and_set_strv(manager):
    assert manager.get_strv("wallpapers") == ["/a.png", "/b.png"]
    manager.set_strv("wallpapers", ["/c.png"])
    assert manager.get_strv("wallpapers") == ["/c.png"]


def test_set_unknown_key_does_not_raise(manager):
    # Hatalı anahtarda istisna fırlatmamalı, False dönmeli
    assert manager.set("yok-boyle-bir-anahtar", "x") is False
