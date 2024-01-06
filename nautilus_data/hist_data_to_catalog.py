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

import requests
from nautilus_trader.persistence.catalog import ParquetDataCatalog
from nautilus_trader.persistence.wranglers import QuoteTickDataWrangler
from nautilus_trader.test_kit.providers import CSVTickDataLoader
from nautilus_trader.test_kit.providers import TestInstrumentProvider

from nautilus_data.util import CATALOG_DIR


def load_fx_hist_data(filename: str, currency: str, catalog_path: str) -> None:
    instrument = TestInstrumentProvider.default_fx_ccy(currency)
    wrangler = QuoteTickDataWrangler(instrument)

    df = CSVTickDataLoader.load(filename, index_col=0, format="%Y%m%d %H%M%S%f")
    df.columns = ["bid_price", "ask_price", "size"]
    print(df)

    ticks = wrangler.process(df)

    catalog = ParquetDataCatalog(catalog_path)
    catalog.write_data([instrument])
    catalog.write_data(ticks)


def download(url: str) -> None:
    filename = url.rsplit("/", maxsplit=1)[1]
    with open(filename, "wb") as f:
        f.write(requests.get(url).content)


def main():
    # Download raw data
    download(
        "https://raw.githubusercontent.com/nautechsystems/nautilus_data/main/raw_data/fx_hist_data/DAT_ASCII_EURUSD_T_202001.csv.gz",
    )
    load_fx_hist_data(
        filename="DAT_ASCII_EURUSD_T_202001.csv.gz",
        currency="EUR/USD",
        catalog_path=CATALOG_DIR,
    )


if __name__ == "__main__":
    main()
