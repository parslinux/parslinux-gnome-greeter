"""Merkezi uygulama sabitleri (AppInfo).

Marka / yol / şema değişikliklerinde güncellenecek TEK dosya budur.
Kod tabanında '/org/parslinux/...' veya 'org.parslinux....' gibi
sabitlerin elle yazılması yerine bu modül kullanılır.

Not: ``RESOURCE_PREFIX`` değeri ``parslinux-gnome-greeter.gresource.xml``
içindeki <prefix> ile birebir aynı olmalıdır.
"""

import os

# Uygulama kimliği (desktop, appdata, gschema ve Gio.Application ile aynı)
APP_ID = "org.parslinux.parslinux-gnome-greeter"

# GResource iç prefix'i (data/*.gresource.xml -> <prefix>)
RESOURCE_PREFIX = "/org/parslinux/parslinux-gnome-greeter"

# Proje adı (meson project_name ile aynı)
PROJECT_NAME = "parslinux-gnome-greeter"

# Kurulum sonrası gresource dosyasının sistem yolu (pkgdatadir ile uyumlu)
INSTALLED_GRESOURCE = f"/usr/share/parslinux/{PROJECT_NAME}/{PROJECT_NAME}.gresource"


def resource_path(*parts: str) -> str:
    """GResource içindeki bir varlığın tam yolunu üretir.

    Örnek:
        resource_path("ui", "MainWindow.ui")
        -> "/org/parslinux/parslinux-gnome-greeter/ui/MainWindow.ui"
    """
    return "/".join((RESOURCE_PREFIX, *parts))


#: GResource yüklenemezse JSON/varlık dosyalarının aranacağı sistem dizinleri
#: (meson install konumları; kurulum ve kaynak ağacı dahil).
DATA_DIRS = [
    f"/usr/share/{PROJECT_NAME}",
    f"/usr/local/share/{PROJECT_NAME}",
]


def data_search_paths(subdir: str, filename: str) -> list:
    """``data/<subdir>/<filename>`` için olası mutlak sistem yollarını üretir."""
    return [os.path.join(d, subdir, filename) for d in DATA_DIRS]


def filesystem_path(*parts: str) -> str:
    """Kaynak ağacındaki (data/) bir dosyanın sistem yolunu üretir.

    Geliştirme modu ve testler için; örn:
        filesystem_path("json", "layout_config.json")
        -> <repo>/data/json/layout_config.json
    """
    import os

    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
    )
    return os.path.join(data_dir, *parts)
