"""Geriye dönük uyumluluk katmanı (deprecated).

Bu modül artık ``.shortcut_manager`` altında yaşıyor (PEP 8 snake_case). Eski
``from ...managers import ShortcutManager`` kullanan üçüncü parti kodları kırmamak
için yalnızca yeniden dışa aktarım yapıyor.
"""

from .shortcut_manager import *  # noqa: F401,F403
from .shortcut_manager import (
    ShortcutManager,
)
