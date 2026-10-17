"""
Manager modules

This module contains manager classes used to manage GNOME desktop settings.
"""

from .shortcut_manager import ShortcutManager
from .theme_manager import ThemeManager
from .wallpaper_manager import WallpaperManager
from .display_manager import DisplayManager
from .extension_manager import ExtensionManager
from .layout_manager import LayoutManager
from .settings import SettingsManager

__all__ = [
    'ShortcutManager',
    'ThemeManager',
    'WallpaperManager',
    'DisplayManager',
    'ExtensionManager',
    'LayoutManager',
    'SettingsManager',
]

