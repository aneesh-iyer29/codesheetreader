import pandas as pd


def to_bool(value):
    """Convert common Excel truthy values to bool."""
    if isinstance(value, bool):
        return value
    if pd.isna(value):
        return False
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() in {"true", "t", "yes", "y", "1"}


def main():
    source_sheet = input("What is the directory of the xlsx sheet? (include the extension): ").strip()
    output_sheet = input("What should the output xlsx be named? (include .xlsx): ").strip()

    df = pd.read_excel(source_sheet, sheet_name="Order")
    # Ignore the first row of the imported sheet.
    df = df.iloc[1:, :]
    df = df.fillna('')

    question_values = df["Value"].tolist()
    bonus_flags = [to_bool(v) for v in df["Bonus"].tolist()]

    cipher_type_flags = []
    for _, row in df.iterrows():
        cipher = str(row.get("Cipher", "")).strip().upper()
        qtype = str(row.get("Type", "")).strip().upper()
        cipher_type_flags.append(cipher == "CRYPTARITHM" or (cipher == "ARISTOCRAT" and qtype == "EXTRACT"))

    output_df = pd.DataFrame([bonus_flags, cipher_type_flags, question_values])
    output_df.to_excel(output_sheet, sheet_name="Scoresheet", index=False, header=False)
    print(f"Wrote scoresheet to {output_sheet}")


if __name__ == "__main__":
    main()