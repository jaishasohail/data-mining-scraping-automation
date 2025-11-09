from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pandas as pd


def _ensure_parent(path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def export_to_csv(items: Iterable[Mapping], path: str | Path) -> Path:
    """
    Export a collection of mapping-like items to a CSV file.
    """
    df = pd.DataFrame(list(items))
    out_path = _ensure_parent(Path(path))
    df.to_csv(out_path, index=False)
    return out_path


def export_to_json(items: Iterable[Mapping], path: str | Path) -> Path:
    """
    Export a collection of mapping-like items to a JSON file.
    """
    df = pd.DataFrame(list(items))
    out_path = _ensure_parent(Path(path))
    df.to_json(out_path, orient="records", indent=2, force_ascii=False)
    return out_path


def export_to_excel(items: Sequence[Mapping], path: str | Path) -> Path:
    """
    Export a sequence of mapping-like items to an Excel file.
    """
    df = pd.DataFrame(list(items))
    out_path = _ensure_parent(Path(path))
    df.to_excel(out_path, index=False)
    return out_path
