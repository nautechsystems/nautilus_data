# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2023 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

import os
import shutil
import tarfile
from pathlib import Path


ROOT = Path(__file__).parent.parent
CATALOG_DIR = ROOT / "catalog"
CATALOG_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR = ROOT / "raw_data"


def tar_dir(path: Path) -> None:
    assert isinstance(path, Path)
    with tarfile.open(f"{path.parent}/{path.stem}.tar.gz", "w:gz") as archive:
        archive.add(str(path), arcname=path.stem, recursive=True)


def remove_catalog_path(catalog_path: str) -> None:
    if os.path.exists(catalog_path):
        shutil.rmtree(catalog_path)
