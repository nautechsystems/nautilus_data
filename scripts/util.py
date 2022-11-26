import os
import shutil
import tarfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
CATALOG_DIR = ROOT / "catalogs"
CATALOG_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR = ROOT / "raw_data"


def tar_dir(path: Path):
    assert isinstance(path, Path)
    with tarfile.open(f"{path.parent}/{path.stem}.tar.gz", "w:gz") as archive:
        archive.add(str(path), arcname=path.stem, recursive=True)


def remove_catalog_path(catalog_path: str):
    if os.path.exists(catalog_path):
        shutil.rmtree(catalog_path)
