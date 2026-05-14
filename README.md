# Nautilus Data (Decommissioned)

This repository has been decommissioned.

Decommissioned: 2026-05.

Example datasets for NautilusTrader now live under the standard test-data layout in the
main `nautechsystems/nautilus_trader` repository.

## Why this changed

This repository predated the current NautilusTrader test-data policy. Keeping it separate
created a second path for fixture data, package metadata, and container builds. The main
repository now provides the policy, checksum registry, metadata sidecars, helper functions,
and public R2 hosting for curated large datasets.

Decommissioning this repository:

- Keeps test data discovery in one place.
- Retires the old `nautilus_data` package and container build path.
- Preserves the EURUSD.SIM sample catalog through the public R2 test-data bucket.
- Keeps raw HISTDATA source files user-fetched instead of redistributing them here.

Existing package or container artifacts, if any, should be treated as frozen historical
artifacts. The `nautilus_data` Python package API is not maintained here.

## Where the data moved

The former EURUSD.SIM catalog data is available as Nautilus Parquet:

- https://test-data.nautechsystems.io/large/histdata_EURUSD.SIM_2020-01_quotes.parquet
- https://test-data.nautechsystems.io/large/histdata_EURUSD.SIM_2020-01_instrument.parquet

Checksums and provenance metadata live in the main repository:

- `tests/test_data/large/checksums.json`
- `tests/test_data/large/histdata_EURUSD.SIM_2020-01_quotes.metadata.json`
- `tests/test_data/large/histdata_EURUSD.SIM_2020-01_instrument.metadata.json`

Rust helpers are available from `nautilus_testkit::common`:

- `ensure_histdata_eurusd_quotes_parquet()`
- `ensure_histdata_eurusd_instrument_parquet()`

There is no replacement `nautilus_data.hist_data_to_catalog` Python API. Python users should
use the main repository's test-data docs and the R2 files above.

## Test-data policy

Use the NautilusTrader developer guide for current dataset rules:

- https://nautilustrader.io/docs/latest/developer_guide/test_datasets/

Large curated datasets should be hosted through the public test-data bucket and recorded in
`tests/test_data/large/checksums.json`. Datasets with redistribution limits should use the
user-fetched workflow documented in the developer guide.

## Raw HISTDATA files

Raw HISTDATA CSV files are not mirrored here. Download them directly from histdata.com when
following examples or tests that require user-fetched source data.

This repository remains only as a historical pointer for old links, tutorials, and old
`pip install nautilus_data` instructions.
