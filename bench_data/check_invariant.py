import sys

import pandas as pd


def check_file(file_name):
    """
    Check if the 'start_ts' column is in ascending order and 'end_ts' for a row
    groups comes before 'start_ts' of the next row group.

    """
    df = pd.read_csv(file_name)

    # Check if 'start_ts' is in ascending order
    if not df["start_ts"].is_monotonic_increasing:
        print("The 'start_ts' column is not in ascending order.")

    # Check if 'end_ts' for a row comes before 'start_ts' of the next row
    for i in range(1, len(df)):
        if df.loc[i - 1, "end_ts"] > df.loc[i, "start_ts"]:
            print(f"Row {i-1} and {i} fail the check:")
            print(df.loc[[i - 1, i]])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_invariant.py <csv_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    check_file(input_file)
