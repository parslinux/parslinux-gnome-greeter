"""Pytest konfigürasyonu.

Bu projenin modülleri PyGObject (gi) üzerinden GTK4/Adw'a bağımlıdır ve
`managers/settings.py` içe aktarım anında Gio.Settings kullanır. Test
ortamında gi kütüphaneleri bulunmadığında, importların başarısız olmaması
için çalışan sahte (mock) nesneler enjekte edilir. Böylece saf Python
mantığı (SettingsManager vb.) izole şekilde test edilebilir.
"""

import sys
import types


class _AnyAttr:
    """Her özniteliğe erişilebilen, çağrılabilir sahte nesne."""

    def __getattr__(self, name):
        return _AnyAttr()

    def __call__(self, *args, **kwargs):
        return _AnyAttr()

    def __iter__(self):
        return iter(())


def _ensure_gi_stubs():
    """gi kütüphanesi yoksa/eksikse çalışabilir sahte modüller kur."""
    try:
        import gi  # noqa: F401
    except ImportError:
        gi_mod = types.ModuleType("gi")
        gi_mod.require_version = lambda *args, **kwargs: None
        sys.modules["gi"] = gi_mod

    try:
        from gi.repository import Gio  # noqa: F401
        ok = hasattr(Gio, "Settings") and hasattr(Gio.Settings, "new")
    except (ImportError, AttributeError, ValueError):
        ok = False

    if not ok:
        try:
            from gi.repository import Gio as _real_gio
        except Exception:
            _real_gio = None
        if _real_gio is not None:
            # Gio kurulu ama Settings.new çalışmıyor → sadece Settings'i ekle
            class _FakeSettings:
                @staticmethod
                def new(schema_id):
                    return _AnyAttr()
            _real_gio.Settings = _FakeSettings
        else:
            repo = types.ModuleType("gi.repository")
            for name in ("Gtk", "Adw", "Gio", "GLib", "Pango", "Gdk", "GdkPixbuf"):
                setattr(repo, name, _AnyAttr())
            sys.modules["gi.repository"] = repo
            return True
    return not ok


GI_STUBBED = _ensure_gi_stubs()


def _ensure_third_party_stubs():
    """pydbus gibi harici bağımlılıklar yoksa sahte modül enjekte et."""
    for name in ("pydbus", "dbus"):
        try:
            __import__(name)
        except ImportError:
            mod = types.ModuleType(name)
            mod.SessionBus = _AnyAttr()
            mod.SystemBus = _AnyAttr()
            sys.modules[name] = mod


_ensure_third_party_stubs()
