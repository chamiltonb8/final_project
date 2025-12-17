import argparse
import pandas as pd
from stat386stonks import clean_prices

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--infile", required=True)
    p.add_argument("--outfile", required=True)
    args = p.parse_args()

    df = pd.read_csv(args.infile)
    df_clean = clean_prices(df)
    df_clean.to_csv(args.outfile, index=False)

if __name__ == "__main__":
    main()