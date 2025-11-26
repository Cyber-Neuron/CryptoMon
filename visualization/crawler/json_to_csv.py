#!/usr/bin/env python3
import csv
import json
import os
from pathlib import Path


def convert_json_to_csv():
    # Get the current script directory
    script_dir = Path(__file__).parent

    # Define input and output file paths
    json_file = script_dir / "result.json"
    csv_file = script_dir / "result.csv"

    try:
        # Read JSON file
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Write to CSV
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(
                [
                    "date",
                    "createTime",
                    "dataType",
                    "id",
                    "price",
                    "remark",
                    "symbol",
                    "volUsd",
                ]
            )

            # Write data
            for entry in data:
                date = entry["date"]
                for item in entry["list"]:
                    writer.writerow(
                        [
                            date,
                            item["createTime"],
                            item["dataType"],
                            item["id"],
                            item["price"],
                            item["remark"],
                            item["symbol"],
                            item["volUsd"],
                        ]
                    )

        print(f"Successfully converted {json_file} to {csv_file}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    convert_json_to_csv()
