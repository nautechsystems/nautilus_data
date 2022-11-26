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
from decimal import Decimal

from nautilus_trader.backtest.node import BacktestNode
from nautilus_trader.config import ImportableStrategyConfig, StreamingConfig
from nautilus_trader.config.backtest import BacktestDataConfig
from nautilus_trader.config.backtest import BacktestEngineConfig
from nautilus_trader.config.backtest import BacktestRunConfig
from nautilus_trader.config.backtest import BacktestVenueConfig
from nautilus_trader.examples.strategies.ema_cross import EMACross
from nautilus_trader.model.data.tick import QuoteTick
from nautilus_trader.persistence.catalog import ParquetDataCatalog

from scripts.util import CATALOG_DIR

if __name__ == "__main__":
    CATALOG_PATH = os.environ.get("CATALOG_PATH", str(CATALOG_DIR))
    catalog = ParquetDataCatalog(CATALOG_PATH)

    # Create a `base` backtest run config object to be shared with all backtests
    base = BacktestRunConfig(
        venues=[
            BacktestVenueConfig(
                name="SIM",
                oms_type="HEDGING",
                account_type="MARGIN",
                base_currency="USD",
                starting_balances=["1000000 USD"],
            ),
        ],
    )

    instrument = catalog.instruments(as_nautilus=True)[0]

    data_config = [
        BacktestDataConfig(
            catalog_path=CATALOG_PATH,
            data_cls=QuoteTick,
            instrument_id=instrument.id.value,
            start_time=1580398089820000000,
            end_time=1580504394501000000,
        ),
    ]

    config = base.update(
        data=data_config,
        engine=BacktestEngineConfig(
            bypass_logging=True,
            strategies=[
                ImportableStrategyConfig(
                    strategy_path=EMACross.fully_qualified_name(),
                    config_path="nautilus_trader.examples.strategies.ema_cross:EMACrossConfig",
                    config=dict(
                        instrument_id=str(instrument.id),
                        bar_type="EUR/USD.SIM-1-MINUTE-MID-INTERNAL",
                        fast_ema_period=10,
                        slow_ema_period=20,
                        trade_size=Decimal(1_000_000),
                        order_id_tag="001",
                    ),
                ),
            ],
            streaming=StreamingConfig(catalog_path=CATALOG_PATH),
        ),
    )

    node = BacktestNode([config])
    node.run()
