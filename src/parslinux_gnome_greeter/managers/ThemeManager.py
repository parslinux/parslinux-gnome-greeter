"""Geriye dönük uyumluluk katmanı (deprecated).

Bu modül artık ``.theme_manager`` altında yaşıyor (PEP 8 snake_case). Eski
``from ...managers import ThemeManager`` kullanan üçüncü parti kodları kırmamak
için yalnızca yeniden dışa aktarım yapıyor.
"""

from .theme_manager import *  # noqa: F401,F403
from .theme_manager import (
    ThemeManager,
)
