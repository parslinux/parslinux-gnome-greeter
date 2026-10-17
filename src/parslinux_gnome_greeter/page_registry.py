"""Sayfa kayıt mekanizması (Page Registry).

Yeni sayfa eklemek için tek adım: ``PAGES`` listesine bir ``PageEntry``
satırı eklemek (+ sayfa sınıfı ve UI dosyası). MainWindow, navigasyonu
bu listeden otomatik kurar.

Sınıflar ITHAL ANINDA değil, İLK KULLANIMDA (lazy) yüklenir; böylece
registry modülü, GTK olmadan da (testlerde) güvenle import edilebilir.
"""

from dataclasses import dataclass
from importlib import import_module
from typing import Callable, List

from locale import gettext as _


@dataclass(frozen=True)
class PageEntry:
    """Bir sihirbaz sayfasının kaydı."""

    name: str          # ViewStack / ListBoxRow adı
    title: str         # Yan panel başlığı (çevirilebilir metin callable'ı)
    icon: str          # Simge adı
    module: str        # Sayfa sınıfının bulunduğu modül
    class_name: str    # Sayfa sınıfının adı

    def load_class(self) -> type:
        """Sayfa sınıfını tembel (lazy) olarak içe aktarır."""
        return getattr(import_module(self.module, package=__package__), self.class_name)


#: Sihirbaz sayfaları, soldan sağa/aşağı sırayla.
PAGES: List[PageEntry] = [
    PageEntry("welcome",      lambda: _("Welcome"),      "go-home-symbolic",                     ".pages.welcome",      "WelcomePage"),
    PageEntry("layout",       lambda: _("Layout"),       "view-paged-symbolic",                  ".pages.layout",       "LayoutPage"),
    PageEntry("theme",        lambda: _("Theme"),        "applications-graphics-symbolic",       ".pages.theme",        "ThemePage"),
    PageEntry("wallpaper",    lambda: _("Wallpaper"),    "image-x-generic-symbolic",             ".pages.wallpaper",    "WallpaperPage"),
    PageEntry("display",      lambda: _("Display"),      "video-display-symbolic",               ".pages.display",      "DisplayPage"),
    PageEntry("extension",    lambda: _("Extensions"),   "org.gnome.Shell.Extensions-symbolic",  ".pages.extension",    "ExtensionPage"),
    PageEntry("applications", lambda: _("Applications"), "view-app-grid-symbolic",               ".pages.applications", "ApplicationsPage"),
    PageEntry("time",         lambda: _("Time"),         "org.gnome.Settings-time-symbolic",     ".pages.time",         "TimePage"),
    PageEntry("outro",        lambda: _("Finish"),       "application-exit-symbolic",            ".pages.outro",        "OutroPage"),
]


def get_pages() -> List[PageEntry]:
    """Sayfa listesini döndürür (sıra = navigasyon sırası)."""
    return PAGES


def page_names() -> List[str]:
    """Kayıtlı sayfa adlarını sırayla döndürür (doğrulama/test için)."""
    return [p.name for p in PAGES]
