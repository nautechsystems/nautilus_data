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

ROOT = os.environ.get("CATALOG_PATH") or Path(__file__).parent.parent
RAW_DATA_DIR = Path(ROOT) / "raw_data"


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


def load_fx_hist_data(filename: str, currency: str, catalog_path: str):
    instrument = TestInstrumentProvider.default_fx_ccy(currency)
    catalog = DataCatalog(catalog_path)
    process_files(
        glob_path=filename,
        reader=TextReader(line_parser=partial(parser, instrument_id=instrument.id)),
        catalog=catalog,
        block_size="10mb",
    )
    # manually write the instrument to the catalog
    write_objects(catalog, [instrument])


def download(url):
    import requests

    filename = url.rsplit("/", maxsplit=1)[1]
    with open(filename, "wb") as f:
        f.write(requests.get(url).content)


def main():
    # Download raw data
    download(
        "https://raw.githubusercontent.com/nautechsystems/nautilus_data/main/raw_data/fx_hist_data/DAT_ASCII_EURUSD_T_202001.csv.gz"
    )
    load_fx_hist_data(
        filename="DAT_ASCII_EURUSD_T_202001*.csv.gz",
        currency="EUR/USD",
        catalog_path=str(ROOT),
    )


if __name__ == "__main__":
    main()
