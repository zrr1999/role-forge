from __future__ import annotations

from pathlib import Path

from role_forge import __version__, __version_tuple__

__all__ = ["__version__", "__version_tuple__"]

__path__ = [str(Path(__file__).resolve().parent.parent / "role_forge")]
