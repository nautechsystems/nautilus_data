import datetime
import os
import shutil
import tarfile
from functools import partial
from pathlib import Path

import pandas as pd
from nautilus_trader.backtest.data.providers import TestInstrumentProvider
from nautilus_trader.core.datetime import dt_to_unix_nanos
from nautilus_trader.model.data.tick import QuoteTick
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.objects import Price, Quantity
from nautilus_trader.persistence.catalog import DataCatalog
from nautilus_trader.persistence.external.core import process_files, write_objects
from nautilus_trader.persistence.external.readers import TextReader

ROOT = Path(__file__).parent.parent
CATALOG_DIR = ROOT / "catalogs"
RAW_DATA_DIR = ROOT / "raw_data"


def tar_dir(path: Path):
    assert isinstance(path, Path)
    with tarfile.open(f"{path.parent}/{path.stem}.tar.gz", "w:gz") as archive:
        archive.add(str(path), arcname=path.stem, recursive=True)


def remove_catalog_path(catalog_path: str):
    if os.path.exists(catalog_path):
        shutil.rmtree(catalog_path)


def parser(line, instrument_id: InstrumentId):
    ts, bid, ask, idx = line.split(b",")
    dt = pd.Timestamp(
        datetime.datetime.strptime(ts.decode(), "%Y%m%d %H%M%S%f"), tz="UTC"
    )
    ts = dt_to_unix_nanos(dt)
    yield QuoteTick(
        instrument_id=instrument_id,
        bid=Price.from_str(bid.decode()),
        ask=Price.from_str(ask.decode()),
        bid_size=Quantity.from_int(100_000),
        ask_size=Quantity.from_int(100_000),
        ts_event=ts,
        ts_init=ts,
    )


def remove_existing_catalog(catalog_path: str):
    full_path = catalog_path + "/catalog"
    # Clear if it already exists, then create fresh
    remove_catalog_path(full_path)
    os.mkdir(full_path)


def load_fx_hist_data(filename: str, currency: str, catalog_path: str):
    instrument = TestInstrumentProvider.default_fx_ccy(currency)
    catalog = DataCatalog(catalog_path)
    process_files(
        glob_path=filename,
        reader=TextReader(line_parser=partial(parser, instrument_id=instrument.id)),
        catalog=catalog,
    )
    # manually write the instrument to the catalog
    write_objects(catalog, [instrument])


if __name__ == "__main__":
    load_fx_hist_data(
        filename=RAW_DATA_DIR / "fx_hist_data/DAT_ASCII_EURUSD_T_202001.csv.gz",
        currency="EUR/USD",
        catalog_path=CATALOG_DIR / "EUDUSD202001",
    )
