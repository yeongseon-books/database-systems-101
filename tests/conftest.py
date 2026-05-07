from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_ko_module(filename: str):
    path = Path(__file__).resolve().parents[1] / "ko" / filename
    spec = importlib.util.spec_from_file_location(filename.replace("-", "_"), path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
