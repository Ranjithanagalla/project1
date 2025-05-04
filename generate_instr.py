import pandas as pd
from datetime import datetime

def generate_instruments_py(input_csv='api-scrip-master.csv', output_py='instruments_list.py'):
    df = pd.read_csv(input_csv, dtype=str)
    today = datetime.now().date()

    df["SEM_EXPIRY_DATE"] = pd.to_datetime(df["SEM_EXPIRY_DATE"], errors='coerce').dt.date

    df_filtered = df[
        (df['SEM_EXPIRY_DATE'] >= today) &
        (df["SEM_INSTRUMENT_NAME"] == "OPTIDX") &
        (df["SEM_EXCH_INSTRUMENT_TYPE"] == "OP") &
        (df['SEM_CUSTOM_SYMBOL'].str.startswith('NIFTY ', na=False))
    ]

    if df_filtered.empty:
        print("❌ No NIFTY expiry data found.")
        return False

    nearest_expiry = sorted(df_filtered["SEM_EXPIRY_DATE"].unique())[0]
    nearest_df = df_filtered[df_filtered["SEM_EXPIRY_DATE"] == nearest_expiry]

    # Extract security IDs
    sec_ids = nearest_df["SEM_SMST_SECURITY_ID"].dropna().unique()

    # Generate Python code
    with open(output_py, 'w') as f:
        f.write("from dhanhq import marketfeed\n")
        f.write("instruments = [\n")
        for secid in sec_ids:
            f.write(f"    (marketfeed.NSE_FNO, \"{secid}\", marketfeed.Ticker),\n")
        f.write("]\n")

    print(f"✅ {output_py} generated with {len(sec_ids)} instruments.")
    return True
generate_instruments_py()   