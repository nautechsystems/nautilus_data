import sys

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


# Define schema for quote ticks
quote_tick_schema = pa.schema(
    [
        ("bid", pa.int64()),
        ("ask", pa.int64()),
        ("bid_size", pa.uint64()),
        ("ask_size", pa.uint64()),
        ("ts_event", pa.uint64()),
        ("ts_init", pa.uint64()),
    ],
)

quote_tick_schema = quote_tick_schema.with_metadata(
    {
        "instrument_id": "EUR/USD.SIM",
        "price_precision": "0",
        "size_precision": "0",
    },
)

trade_tick_schema = pa.schema(
    [
        ("price", pa.int64()),
        ("size", pa.uint64()),
        ("aggresor_side", pa.uint8()),
        ("trade_id", pa.string()),
        ("ts_event", pa.uint64()),
        ("ts_init", pa.uint64()),
    ],
)

trade_tick_schema = trade_tick_schema.with_metadata(
    {
        "instrument_id": "EUR/USD.SIM",
        "price_precision": "0",
        "size_precision": "0",
    },
)


def write_parquet_with_row_group(input_file, output_file, rows_per_row_group):
    """Write a Parquet file with specified row group size."""
    df = pd.read_parquet(input_file)

    schema = quote_tick_schema if "quotes" in input_file else trade_tick_schema

    # Create a new Parquet file writer
    writer = pq.ParquetWriter(output_file, schema, compression="snappy")

    # Write the dataframe to the new Parquet file with specified row group size
    num_rows = len(df)
    for i in range(0, num_rows, rows_per_row_group):
        batch = pa.RecordBatch.from_pandas(df[i : i + rows_per_row_group])
        writer.write_batch(batch)

    # Close the Parquet file writer
    writer.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python extract_ts_init.py <parquet_file> <num_rows_per_row_group>",
        )
        sys.exit(1)

    # Get command-line inputs
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    rows_per_row_group = int(sys.argv[3])

    # Write the Parquet file with specified row group size
    write_parquet_with_row_group(input_file, output_file, rows_per_row_group)
