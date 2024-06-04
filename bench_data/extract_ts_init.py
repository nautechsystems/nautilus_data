import pyarrow.parquet as pq
import csv
import sys


def extract_ts_init_values(parquet_file, csv_file):
    """Write the first and last 'ts_init' values of each row group to a CSV file."""
    # Open the Parquet file
    parquet_file = pq.ParquetFile(parquet_file)

    # Open the CSV file for writing
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["index", "start_ts", "end_ts", "group_size"])  # Write the header

        # Iterate over each row group in the Parquet file
        for i in range(parquet_file.num_row_groups):
            # Read the row group into a table
            table = parquet_file.read_row_group(i)

            # Convert the 'ts_init' column to a list
            ts_init_values = table.column("ts_init").to_pandas().tolist()

            # Write the index, first and last value to the CSV file
            writer.writerow([i, ts_init_values[0], ts_init_values[-1], table.num_rows])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_ts_init.py <parquet_file> <csv_file>")
        sys.exit(1)

    parquet_file = sys.argv[1]
    csv_file = sys.argv[2]

    extract_ts_init_values(parquet_file, csv_file)
