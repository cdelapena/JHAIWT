import sys
from pathlib import Path
from argparse import ArgumentParser
from typing import Dict

from fetch_external_data import fetch_external_data


def parse_args() -> Dict:
    """Argument handler for writing external data to flat file.
        Default output is csv

    Returns:
        Dict: **kwargs
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--file_type",
        type=str,
        default="csv",
        help="output file_type requested",
        required=False,
    )
    return vars(parser.parse_args())


def main(file_type: str) -> None:
    """Fetches external data and stores as a flat file.

    Args:
        file_type (str): output file_type requested
    """

    api_sources = Path.cwd().resolve().joinpath("data").joinpath("api_sources.txt")
    try:
        jobs_df = fetch_external_data(api_sources)
    except:
        raise

    data_path = Path.cwd().resolve().joinpath("data")
    print(f"Writing jobs_df to {data_path} as {file_type}...")
    match file_type:
        case "csv":
            jobs_df.to_csv(data_path.joinpath("Jobs").with_suffix(".csv"), sep=',', lineterminator="\n", index=False)
        case "parquet":
            jobs_df.to_parquet(data_path.joinpath("Jobs").with_suffix(".parquet"), compression="snappy", index=False)

    return


if __name__ == "__main__":
    try:
        args = parse_args()
        main(**args)
    except Exception as e:
        err_msg = f"Ingestion failed: {e}"
        sys.exit(err_msg)
