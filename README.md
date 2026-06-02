## Bank Statement Cleaner

A simple Python CLI tool that cleans messy `.xls` and `.xlsx` bank statement exports and converts them into a clean CSV file ready for import into Actual Budget.

## Features

* Supports `.xls` and `.xlsx` bank statement files
* Automatically removes unnecessary headers and metadata
* Cleans footer information and trailing notes
* Normalizes transaction tables
* Optional transaction order reversal
* Exports clean UTF-8 CSV files
* Designed to be resilient to minor bank statement format changes

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/AgreeableAK/bank-statement-cleaner.git
```

### 2. Change the Directory

```bash
cd bank-statement-cleaner
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the script and provide the path to your bank statement file:

```bash
python statement_cleaner.py -i "path/to/statement.xls"
```
Example: python statement_cleaner.py -i "C:\Users\Your_User\Desktop\bank-statement-cleaner\statement.xls"

### Reverse Transaction Order

If your statement is exported in reverse chronological order and you want the output sorted from oldest to newest:

```bash
python statement_cleaner.py -i "path/to/statement.xls" -r
```
Example: python statement_cleaner.py -i "C:\Users\Your_User\Desktop\bank-statement-cleaner\statement.xls" -r

## Command Line Options

| Option            | Description                                |
| ----------------- | ------------------------------------------ |
| `-i`, `--input`   | Path to the input `.xls` or `.xlsx` file   |
| `-r`, `--reverse` | Reverse transaction order before exporting |

## Example Input and Output

The script automatically creates a cleaned CSV file in the same directory as the source file.

#### Input:

<p align="center">
  <img src="project_screenshot/Example_Statement_Header.png" width="800"/>
</p>
<p align="center">
  <img src="project_screenshot/Example_Statement_Footer.png" width="800"/>
</p>

#### Output:

#### Without "-r" parameter.
<p align="center">
  <img src="project_screenshot/Cleaned_Example_Statement__Without_Reversal.png" width="800"/>
</p>

#### With "-r" Parameter.
<p align="center">
  <img src="project_screenshot/Cleaned_Example_Statement_Reversal.png" width="800"/>
</p>

