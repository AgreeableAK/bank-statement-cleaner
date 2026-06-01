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

def merge_split_remarks(df): # Merges overflow text from empty rows back into the main transaction row.
    merged_rows = []
    
    for index, row in df.iterrows():
        if pd.notna(row['Value Date']):
            merged_rows.append(row.to_dict())
        
        else:
            overflow_text = row['Transaction Remarks']
            
            if pd.notna(overflow_text) and len(merged_rows) > 0:
             
                current_remark = merged_rows[-1]['Transaction Remarks']
                
               
                if pd.isna(current_remark):
                    merged_rows[-1]['Transaction Remarks'] = str(overflow_text).strip()
                else:
                    merged_rows[-1]['Transaction Remarks'] = f"{current_remark} {str(overflow_text).strip()}"
                
    
    return pd.DataFrame(merged_rows)

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

def export_to_csv(df, original_path): # Exports the cleaned dataframe to a CSV file.
    
    new_filename = f"{original_path.stem}_CLEANED.csv"
    
    output_path = original_path.parent / new_filename
    
    df.to_csv(output_path, index=False)
    
    print(f"\nSuccess! Cleaned data exported to: {output_path.name}")
    return output_path

if __name__ == "__main__":
    file_path = Path("~\\Documents\\Projects\\bank-statement-cleaner\\OpTransactionHistory29-05-2026(Redacted).xls")
    raw_data = load_statement(file_path)

    if raw_data is not None:
        start_row = find_table_start(raw_data)
        
        if start_row is not None:
            # 1. Remove the headers and junk rows above the transaction table, and set the first row as column names
            transaction_table = extract_table(raw_data, start_row)
            
            # 2. Normalize columns first so we have clean names (like 'Value Date')
            normalized_table = normalize_table(transaction_table)
            
            # 3. Merge split remarks (This automatically ignores footers!)
            merged_remarks_table = merge_split_remarks(normalized_table)
            
            # 4. Reverse chronological order
            chronological_table = reverse_transactions(merged_remarks_table)
            
            # 5. Export the cleaned table to CSV
            export_to_csv(chronological_table, file_path)