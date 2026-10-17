"""Sayfa kayıt ve temel modül testleri (page_registry, appinfo, interfaces)."""

from parslinux_gnome_greeter import appinfo, page_registry
from parslinux_gnome_greeter.interfaces import (
    DisplayProviderProtocol,
    ExtensionProviderProtocol,
    LayoutProviderProtocol,
    SettingsProtocol,
    ThemeProviderProtocol,
    WallpaperProviderProtocol,
)


def test_appinfo_constants():
    """Uygulama kimliği ve yollar doğru tanımlı olmalı."""
    assert appinfo.APP_ID == "org.parslinux.parslinux-gnome-greeter"
    assert appinfo.RESOURCE_PREFIX == "/org/parslinux/parslinux-gnome-greeter"
    assert appinfo.PROJECT_NAME == "parslinux-gnome-greeter"


def test_appinfo_resource_path():
    """GResource yolu prefix ile doğru birleştirilmeli."""
    path = appinfo.resource_path("ui", "MainWindow.ui")
    assert path == "/org/parslinux/parslinux-gnome-greeter/ui/MainWindow.ui"


def test_appinfo_filesystem_path():
    """Geliştirme dizinindeki data/ yolu üretilebilmeli."""
    path = appinfo.filesystem_path("json", "layout_config.json")
    assert path.endswith("data/json/layout_config.json")


def test_page_registry_entries():
    """Kayıtlı 9 sayfa sırayla mevcut olmalı."""
    expected = [
        "welcome",
        "layout",
        "theme",
        "wallpaper",
        "display",
        "extension",
        "applications",
        "time",
        "outro",
    ]
    assert page_registry.page_names() == expected
    pages = page_registry.get_pages()
    assert len(pages) == len(expected)


def test_page_registry_load_classes():
    """Her sayfa tanımı kendi sınıfını başarıyla yükleyebilmeli."""
    for entry in page_registry.get_pages():
        cls = entry.load_class()
        assert cls is not None
        assert cls.__name__ == entry.class_name
        # Başlık fonksiyonu çağrılabilir olmalı
        assert isinstance(entry.title(), str)


def test_main_window_lazy_loading():
    """MainWindow açıldığında yalnızca talep edilen sayfa yüklenmeli (on-demand / lazy)."""
    from parslinux_gnome_greeter.main_window import MainWindow

    win = MainWindow.__new__(MainWindow)
    win._pages_by_name = {entry.name: entry for entry in page_registry.get_pages()}
    win._page_instances = {}
    win.view_stack = type("FakeViewStack", (), {"add_named": lambda self, w, n: None})()
    win._on_navigate_request = lambda *a: None

    # Başlangıçta hiç sayfa yüklenmemiş olmalı
    assert len(win._page_instances) == 0

    # Welcome sayfası yüklendiğinde sadece o eklenmeli
    p1 = win._ensure_page("welcome")
    assert p1 is not None
    assert "welcome" in win._page_instances
    assert len(win._page_instances) == 1

    # Tekrar istendiğinde önbellekten aynı nesne dönmeli
    p1_cached = win._ensure_page("welcome")
    assert p1 is p1_cached
    assert len(win._page_instances) == 1

    # Layout sayfasına geçildiğinde lazy olarak yüklenmeli
    p2 = win._ensure_page("layout")
    assert p2 is not None
    assert "layout" in win._page_instances
    assert len(win._page_instances) == 2

