"""
anomaly_detector_hennelly.py - Project script (example).

Author: Kevin Hennelly
Date: 2026-03-14

Static Data

- Data is taken from a pediatric clinic's patient records.
- The data is static, meaning it does not change over time and is not updated with new records.
- The clinic works with children from birth to 16 years old.
- Each row represents a patient visit with two key measurements:
  - age_years: The patient's age in years.
  - height_inches: The patient's height in inches.

Purpose

- Read the data from a CSV (comma-separated values) file.
- Detect anomalies.
- Log the pipeline process to assist with debugging and transparency.

Paths (relative to repo root)

    INPUT FILE: data/clinic_data_hennelly.csv
    OUTPUT FILE: artifacts/anomalies_hennelly.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.anomaly_detector_hennelly

OBS:
  Copy of anomally_detector_case.py for adding modifications for class assignments.
"""

# === DECLARE IMPORTS (packages we will use in this project) ===

# First from the Python standard library (no installation needed)
import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P2", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS FOR FOLDER PATHS (directories) ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

# === DECLARE GLOBAL CONSTANTS FOR FILE PATHS ===

DATA_FILE: Final[Path] = DATA_DIR / "clinic_data_hennelly.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "anomalies_hennelly.csv"


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the pipeline.

    log_header() logs a standard run header.
    log_path() logs repo-relative paths (privacy-safe).
    """
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    # Log the constants to help with debugging and transparency.
    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    # Call the mkdir() method to ensure it exists
    # The parents=True argument allows it to create any necessary parent directories.
    # The exist_ok=True argument prevents an error if the directory already exists.
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ CSV DATA FILE INTO A POLARS DATAFRAME (TABLE)
    # ----------------------------------------------------
    # Polars is great for tabular data.
    # We will use the polars package to
    # read csv (comma-separated values) files
    # into a two dimensional table (DataFrame).

    # Call the polars library read_csv() method.
    # Pass in (provide) the DATA_FILE path of the CSV file.
    # Name the result "df" as is customary.
    df: pl.DataFrame = pl.read_csv(DATA_FILE)

    # Visually inspect the file in the data/ folder.
    # It has columns named `age_years` and `height_inches`.
    # The DataFrame height attribute returns the number of rows.
    LOG.info(f"Loaded {df.height} patient records")

    # ----------------------------------------------------
    # STEP 2: DEFINE THRESHOLDS AND DETECT ANOMALIES
    # ----------------------------------------------------
    # An anomaly is any value greater than the threshold we set.
    # Domain rule for this example:
    # Anything above this value is suspicious.
    LOG.info("Studying children's ages and heights to find anomalies...")

    # x is age in years, so 16 is the upper limit for kids
    MAX_REASONABLE_X_VALUE: Final[float] = 16.0

    # y is height in inches, so maybe 6 feet (72 inches) is a reasonable upper limit
    MAX_REASONABLE_Y_VALUE: Final[float] = 72.0

    LOG.info(f"MAX_REASONABLE_X_VALUE: {MAX_REASONABLE_X_VALUE} in years")
    LOG.info(f"MAX_REASONABLE_Y_VALUE: {MAX_REASONABLE_Y_VALUE} in inches")

    # Create a new DataFrame named anomalies_df that contains
    # only the rows where EITHER
    # the age is TOO HIGH OR
    # the height is TOO HIGH.
    # A single pipe (|) is the OR operator in polars.
    # We will use greater than or equal to (>=) to find values at or above the threshold.
    anomalies_df: pl.DataFrame = df.filter(
        (pl.col("age_years") >= MAX_REASONABLE_X_VALUE)
        | (pl.col("height_inches") >= MAX_REASONABLE_Y_VALUE)
    )

    # Added code by Kevin Hennelly for Week 2 Custom Project.
    # This categorizes how extreme each anomaly is based on how much it exceeds the threshold.

    # === ADD SEVERITY LEVEL TO ANOMALIES ===
    # Severity is based on how far outside the valid range each value is

    def classify_age_severity(age):
        if age <= 16:
            return "none"
        elif age <= 18:
            return "mild"
        elif age <= 21:
            return "moderate"
        else:
            return "severe"

    def classify_height_severity(height):
        if height <= 72:
            return "none"
        elif height <= 75:
            return "mild"
        elif height <= 80:
            return "moderate"
        else:
            return "severe"

    SEVERITY_RANK = {"none": 0, "mild": 1, "moderate": 2, "severe": 3}

    def overall_severity(age, height):
        age_sev = classify_age_severity(age)
        height_sev = classify_height_severity(height)
        if SEVERITY_RANK[age_sev] >= SEVERITY_RANK[height_sev]:
            return age_sev
        return height_sev

    anomalies_df = anomalies_df.with_columns(
        [
            pl.struct(["age_years", "height_inches"])
            .map_elements(
                lambda row: overall_severity(row["age_years"], row["height_inches"]),
                return_dtype=pl.String,
            )
            .alias("severity_level"),
            pl.col("age_years")
            .map_elements(classify_age_severity, return_dtype=pl.String)
            .alias("age_severity"),
            pl.col("height_inches")
            .map_elements(classify_height_severity, return_dtype=pl.String)
            .alias("height_severity"),
        ]
    )

    # Update LOG.info for Week 2 Project to include severity breakdown.
    LOG.info(
        f"Count of anomalies found: {anomalies_df.height} | Severity breakdown: {anomalies_df['severity_level'].value_counts()}"
    )

    # ----------------------------------------------------
    # STEP 3: SAVE THE OUTPUT ANOMALIES AS EVIDENCE
    # ----------------------------------------------------
    # We call generated files "artifacts".
    # They are important evidence of the work we did and the results we found.
    # We will save the anomalies_df DataFrame as a CSV file in the artifacts/ folder

    # Every Polars DataFrame has a write_csv() method that saves it as a CSV file.
    # Just pass in the full Path to the file you want to create.
    anomalies_df.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote anomalies file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
