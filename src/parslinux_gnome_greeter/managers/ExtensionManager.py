"""Geriye dönük uyumluluk katmanı (deprecated).

Bu modül artık ``.extension_manager`` altında yaşıyor (PEP 8 snake_case). Eski
``from ...managers import ExtensionManager`` kullanan üçüncü parti kodları kırmamak
için yalnızca yeniden dışa aktarım yapıyor.
"""

from .extension_manager import *  # noqa: F401,F403
from .extension_manager import (
    ExtensionManager,
)
