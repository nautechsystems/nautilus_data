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

import datetime
from functools import partial

import pandas as pd
import requests
from nautilus_trader.backtest.data.providers import TestInstrumentProvider
from nautilus_trader.core.datetime import dt_to_unix_nanos
from nautilus_trader.model.data.tick import QuoteTick
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.objects import Price, Quantity
from nautilus_trader.persistence.catalog import ParquetDataCatalog
from nautilus_trader.persistence.external.core import process_files, write_objects
from nautilus_trader.persistence.external.readers import TextReader


def parser(line, instrument_id: InstrumentId):
    ts, bid, ask, idx = line.split(b",")
    dt = pd.Timestamp(
        datetime.datetime.strptime(ts.decode(), "%Y%m%d %H%M%S%f"),
        tz="UTC",
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
    catalog = ParquetDataCatalog(catalog_path)
    process_files(
        glob_path=filename,
        reader=TextReader(line_parser=partial(parser, instrument_id=instrument.id)),
        catalog=catalog,
        block_size="10mb",
    )
    # manually write the instrument to the catalog
    write_objects(catalog, [instrument])


def download(url):

    filename = url.rsplit("/", maxsplit=1)[1]
    with open(filename, "wb") as f:
        f.write(requests.get(url).content)


def main():
    # Download raw data
    download(
        "https://raw.githubusercontent.com/nautechsystems/nautilus_data/main/raw_data/fx_hist_data/DAT_ASCII_EURUSD_T_202001.csv.gz",
    )
    load_fx_hist_data(
        filename="DAT_ASCII_EURUSD_T_202001*.csv.gz",
        currency="EUR/USD",
        catalog_path="catalog",
    )


if __name__ == "__main__":
    main()
