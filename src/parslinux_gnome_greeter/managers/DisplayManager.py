"""Geriye dönük uyumluluk katmanı (deprecated).

Bu modül artık ``.display_manager`` altında yaşıyor (PEP 8 snake_case). Eski
``from ...managers import DisplayManager`` kullanan üçüncü parti kodları kırmamak
için yalnızca yeniden dışa aktarım yapıyor.
"""

from .display_manager import *  # noqa: F401,F403
from .display_manager import (
    DisplayManager,
)
