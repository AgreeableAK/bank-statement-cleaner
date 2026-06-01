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


def extract_table(df, start_index): #Remove junk rows above the table and set the first row as header

    cleaned_df = df.iloc[start_index:].copy()

    cleaned_df.columns = cleaned_df.iloc[0]

    cleaned_df = cleaned_df[1:]
    cleaned_df = cleaned_df.reset_index(drop=True)

    return cleaned_df

def remove_footer(df):
    
    total_columns = len(df.columns)
    
    minimum_valid_cells = total_columns // 2 
    
    clean_df = df.dropna(thresh=minimum_valid_cells).copy()
    
    rows_dropped = len(df) - len(clean_df)
    print(f"Dropped {rows_dropped} footer/empty rows.")
    
    return clean_df.reset_index(drop=True)

def normalize_table(df): # Cleans up columns by removing completely empty ones and stripping whitespace.
    
    normalized_df = df.dropna(axis=1, how='all').copy()
    
    clean_columns = []
    for col in normalized_df.columns:
  
        clean_col_name = str(col).strip()
        clean_columns.append(clean_col_name)
        

    normalized_df.columns = clean_columns
    
    return normalized_df

def reverse_transactions(df): # Reverses the row order of the dataframe so oldest transactions are first.
    
    reversed_df = df.iloc[::-1].copy()
    reversed_df = reversed_df.reset_index(drop=True)
    
    return reversed_df

if __name__ == "__main__":

    file_path = Path("~\\Documents\\Projects\\bank-statement-cleaner\\OpTransactionHistory29-05-2026(Redacted).xls")
    df = load_statement(file_path)

    raw_data = load_statement(file_path)


    if raw_data is not None:
        start_row = find_table_start(raw_data)
        
        if start_row is not None:
            transaction_table = extract_table(raw_data, start_row)
            transactions_only = remove_footer(transaction_table)
            final_clean_table = normalize_table(transactions_only)
            chronological_table = reverse_transactions(final_clean_table)
            
            print("\nFully Normalized Table:")
            print(chronological_table.head())
            print(f"\nRemaining Columns: {list(chronological_table.columns)}")