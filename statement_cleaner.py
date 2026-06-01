import pandas as pd
from pathlib import Path

def load_statement(file_path):

    try:
        df = pd.read_excel(file_path, header=None)
        print(f"Successfully Loaded: {file_path}")
        print(f"The file has {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Unexpected error loading file: {e}")
        return None
    

def find_table_start(df):

    keywords = ["date","s no.","cheque", "description", "amount", "balance", "withdrawal", "deposit", "transaction"]

    for index, row in df.head(50).iterrows():

        match_count = 0

        for cell in row:

            if pd.isna(cell):
                continue

            cell_text = str(cell).lower()

            for keyword in keywords:
                if keyword in cell_text:
                    match_count += 1
                    break

        if match_count >= 5:
            print(f"Table header found at row index: {index}")
            return index
    print(f"Error: Could not find start of transaction table. Please check the file format.")


def extract_table(df, start_index):

    cleaned_df = df.iloc[start_index:].copy()

    cleaned_df.columns = cleaned_df.iloc[0]

    cleaned_df = cleaned_df[1:]
    cleaned_df = cleaned_df.reset_index(drop=True)

    return cleaned_df

if __name__ == "__main__":

    file_path = Path("~\\Documents\\Projects\\bank-statement-cleaner\\OpTransactionHistory29-05-2026(Redacted).xls")
    df = load_statement(file_path)

    raw_data = load_statement(file_path)


    if raw_data is not None:
    
        start_row = find_table_start(raw_data)
        
        if start_row is not None:
            transaction_table = extract_table(raw_data, start_row)
            
            # Print the first 5 rows to verify it worked!
            print("\nExtracted Table Preview:")
            print(transaction_table.head()) 