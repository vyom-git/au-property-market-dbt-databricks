import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/nsw_property_sales.csv")


def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Could not find {RAW_FILE}")

    df = pd.read_csv(RAW_FILE, nrows=1000)

    print("\nColumns:")
    for col in df.columns:
        print(f"- {col}")

    print("\nSample rows:")
    print(df.head())

    print("\nSample shape:")
    print(df.shape)

    print("\nData types:")
    print(df.dtypes)


if __name__ == "__main__":
    main()