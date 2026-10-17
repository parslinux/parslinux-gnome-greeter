"""Geriye dönük uyumluluk katmanı (deprecated).

Bu modül artık ``.wallpaper_manager`` altında yaşıyor (PEP 8 snake_case). Eski
``from ...managers import WallpaperManager`` kullanan üçüncü parti kodları kırmamak
için yalnızca yeniden dışa aktarım yapıyor.
"""

from .wallpaper_manager import *  # noqa: F401,F403
from .wallpaper_manager import (
    WallpaperManager,
)
