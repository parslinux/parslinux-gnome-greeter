"""Geriye dönük uyumluluk katmanı (deprecated).

Bu modül artık ``.layout_manager`` altında yaşıyor (PEP 8 snake_case). Eski
``from ...managers import LayoutManager`` kullanan üçüncü parti kodları kırmamak
için yalnızca yeniden dışa aktarım yapıyor.
"""

from .layout_manager import *  # noqa: F401,F403
from .layout_manager import (
    LayoutManager,
)
