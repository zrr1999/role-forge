from __future__ import annotations

import sys
from pathlib import Path

from role_forge._version import __version__, __version_tuple__

__all__ = ["__version__", "__version_tuple__"]

__path__ = [str(Path(__file__).resolve().parent)]
sys.modules.setdefault("agent_caster", sys.modules[__name__])
