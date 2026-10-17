"""Soyut arayüzler (Protocols).

Manager sınıflarının beklenen sözleşmelerini tip-tabanlı olarak tanımlar.
Bu sayede:

* Sayfalar somut sınıflara değil, sözleşmelere bağlanabilir → mock ile
  test yazmak kolaylaşır (mypy ile statik kontrol).
* Greeter → gerçek login ekranı geçişinde sayfaları değiştirmeden farklı
  manager implementasyonları takılabilir.

Not: ``typing.Protocol`` yapısal (duck) tiplendirme sağlar; mevcut
sınıflarda hiçbir değişiklik gerektirmez.
"""

from typing import Any, Dict, List, Protocol, runtime_checkable


@runtime_checkable
class SettingsProtocol(Protocol):
    """GSettings benzeri anahtar/değer erişimi (bkz. SettingsManager)."""

    def get(self, key: str) -> Any: ...

    def set(self, key: str, value: Any) -> bool: ...

    def get_strv(self, key: str) -> List[str]: ...

    def set_strv(self, key: str, value: List[str]) -> bool: ...


@runtime_checkable
class ThemeProviderProtocol(Protocol):
    """Tema / vurgu rengi uygulamaktan sorumlu manager sözleşmesi.

    Uyumluluk: ``managers.theme_manager.ThemeManager``
    """

    def get_current_color_scheme(self) -> str: ...

    def set_color_scheme(self, scheme: str) -> None: ...

    def set_gtk_theme(self, theme: str) -> None: ...

    def set_icon_theme(self, theme: str) -> None: ...

    def set_accent_color(self, color_name: str) -> None: ...

    def add_accent_color_callback(self, callback) -> None: ...


@runtime_checkable
class WallpaperProviderProtocol(Protocol):
    """Duvar kağıdı listeleme / uygulama sözleşmesi.

    Uyumluluk: ``managers.wallpaper_manager.WallpaperManager``
    """

    def get_wallpapers(self) -> List[Any]: ...

    def set_wallpaper(self, file_path: str) -> Any: ...

    def get_current_wallpaper(self) -> Any: ...


@runtime_checkable
class ExtensionProviderProtocol(Protocol):
    """GNOME eklentilerini okuma/etkinleştirme sözleşmesi.

    Uyumluluk: ``managers.extension_manager.ExtensionManager``
    """

    def get_extensions(self) -> List[Dict[str, Any]]: ...

    def enable_extension(self, extension_id: str) -> bool: ...

    def disable_extension(self, extension_id: str) -> bool: ...

    def is_extension_enabled(self, extension_id: str) -> bool: ...


@runtime_checkable
class LayoutProviderProtocol(Protocol):
    """Yerleşim (panel/dock) yapılandırma sözleşmesi.

    Uyumluluk: ``managers.layout_manager.LayoutManager``
    """

    def get_available_layouts(self) -> List[Any]: ...

    def get_current_layout(self) -> Any: ...

    def apply_layout(self, layout_name: str) -> Any: ...


@runtime_checkable
class DisplayProviderProtocol(Protocol):
    """Ekran çözünürlük/oran yönetimi sözleşmesi.

    Uyumluluk: ``managers.display_manager.DisplayManager``
    (monitör bilgisi asenkron callback ile verilir)
    """

    def get_monitors(self, callback) -> None: ...

    def apply_resolution_change(self, monitor_id: Any, mode_id: Any) -> Any: ...

    def apply_scale_change(self, monitor_id: Any, mode_id: Any, new_scale: Any) -> Any: ...
