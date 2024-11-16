import os
import sys
import warnings
import argparse


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
warnings.filterwarnings("ignore")

from src.preprocess_text import PreprocessText


def main():
    # Parses the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        required=True,
        help="Enter name of language for which datasets should be downloaded. Current options: 'es', fr' or 'de'.",
    )
    parser.add_argument(
        "-ntps",
        "--n_texts_per_subset",
        type=str,
        required=True,
        help="Enter power of 2 for no. of texts in a subset (E.g.: 16).",
    )
    parser.add_argument(
        "-pdv",
        "--processed_dataset_version",
        type=str,
        required=True,
        help="Enter version for storing the processed dataset.",
    )
    args = parser.parse_args()

    # Checks if the arguments, have valid values.
    assert args.language in [
        "es",
        "fr",
        "de",
    ], "Argument language should have value as 'es', 'fr', or 'de'."


if __name__ == "__main__":
    main()
