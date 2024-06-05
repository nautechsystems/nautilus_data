import csv
import os
import sys

import pyarrow.parquet as pq


def record_data_stats(folder_path, csv_file):
    """Record statistics about Parquet files in a folder."""
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["file_name", "file_size_kb", "total_rows", "max_row_group_size"],
        )  # Write the header

        # Walk the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".parquet"):
                    file_path = os.path.join(root, file)

                    # Calculate file size in KB
                    file_size_kb = os.path.getsize(file_path) // 1024

                    # Read the Parquet file
                    parquet_file = pq.ParquetFile(file_path)

                    # Calculate total number of rows and maximum row group size
                    total_rows = 0
                    max_row_group_size = 0
                    for i in range(parquet_file.num_row_groups):
                        row_group = parquet_file.read_row_group(i)
                        num_rows = row_group.num_rows
                        total_rows += num_rows
                        max_row_group_size = max(max_row_group_size, num_rows)

                    # Write the statistics to the CSV file
                    writer.writerow(
                        [file_path, file_size_kb, total_rows, max_row_group_size],
                    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <folder_path> <csv_file>")
        sys.exit(1)

    folder_path = sys.argv[1]
    csv_file = sys.argv[2]

    record_data_stats(folder_path, csv_file)
