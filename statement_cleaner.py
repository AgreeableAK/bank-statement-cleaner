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
    
if __name__ == "__main__":

    file_path = Path("~\\Documents\\Projects\\bank-statement-cleaner\\OpTransactionHistory29-05-2026(Redacted).xls")
    df = load_statement(file_path)