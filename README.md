# nautilus_data

Example market data for use with NautilusTrader.

## Installation

```bash
uv pip install nautilus_data
```

## Requirements

- Python 3.13+
- NautilusTrader 1.220.0+

## Usage

This package provides sample market data that can be used for backtesting and development with the NautilusTrader platform.

## Data

The package includes historical foreign exchange (FX) tick data:

- **EUR/USD** - January 2020 tick-level bid/ask quotes
- Format: CSV compressed with gzip.
- Source: Publicly available FX market data.

### Loading data into a catalog

```python
from nautilus_data.hist_data_to_catalog import load_data

# Load historical data into your NautilusTrader catalog
load_data()
```

## Structure

- `catalog/` - Pre-processed data catalog files (once `hist_data_to_catalog.py` is run).
- `raw_data/` - Raw historical data files.
- `bench_data/` - Benchmark data for performance testing.

## More Information

For more information about NautilusTrader, visit [nautechsystems.io](https://nautechsystems.io).
