#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2022 Nautech Systems Pty Ltd. All rights reserved.
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
import pathlib
from decimal import Decimal

from nautilus_trader.backtest.config import BacktestDataConfig
from nautilus_trader.backtest.config import BacktestEngineConfig
from nautilus_trader.backtest.config import BacktestRunConfig
from nautilus_trader.backtest.config import BacktestVenueConfig
from nautilus_trader.backtest.node import BacktestNode
from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig
from nautilus_trader.persistence.catalog import DataCatalog
from nautilus_trader.persistence.config import PersistenceConfig
from nautilus_trader.trading.config import ImportableStrategyConfig


if __name__ == "__main__":

    CATALOG_PATH = os.environ.get("CATALOG_PATH") or str(
        pathlib.Path("../catalogs/EUDUSD202001").resolve()
    )
    catalog = DataCatalog(CATALOG_PATH)

    # Create a `base` config object to be shared with all backtests
    base = BacktestRunConfig(
        venues=[
            BacktestVenueConfig(
                name="SIM",
                oms_type="HEDGING",
                account_type="MARGIN",
                base_currency="USD",
                starting_balances=["1000000 USD"],
            )
        ]
    )

    instrument = catalog.instruments(as_nautilus=True)[0]

    data_config = [
        BacktestDataConfig(
            catalog_path=CATALOG_PATH,
            data_cls_path="nautilus_trader.model.data.tick.QuoteTick",
            instrument_id=instrument.id.value,
            start_time=1580398089820000000,
            end_time=1580504394501000000,
        )
    ]

    config = base.update(
        data=data_config,
        engine=BacktestEngineConfig(bypass_logging=True),
        strategies=[
            ImportableStrategyConfig(
                path="nautilus_trader.examples.strategies.ema_cross:EMACross",
                config=EMACrossConfig(
                    instrument_id=str(instrument.id),
                    bar_type="EUR/USD.SIM-1-MINUTE-MID-INTERNAL",
                    fast_ema_period=10,
                    slow_ema_period=20,
                    trade_size=Decimal(1_000_000),
                    order_id_tag="001",
                ),
            ),
        ],
        persistence=PersistenceConfig(catalog_path=CATALOG_PATH, kind="backtest"),
    )

    node = BacktestNode()
    node.run_sync([config])
