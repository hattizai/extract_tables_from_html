# HTML Table Extractor

## Description
This Python script extracts tables from HTML files and converts them into Excel spreadsheets. It handles hyperlinks by creating separate URL columns and can add a custom 'type' column to all extracted tables.

## Features
- Extracts all tables from a given HTML file
- Preserves hyperlinks by creating separate URL columns
- Adds a custom 'type' column to all tables
- Outputs data to an Excel file with multiple sheets (one per table)
- Prepends "https://scan.merlinchain.io" to all extracted URLs

## Requirements
- Python 3.x
- pandas
- BeautifulSoup4
- openpyxl

## Usage
Run the script from the command line with two arguments:
1. Path to the HTML file
2. Value for the 'type' column


## Output
The script generates an Excel file named '[original_filename]_tables.xlsx' in the same directory as the input HTML file. Each table from the HTML file is placed in a separate sheet within the Excel file.

## Main Functions
- `read_html_file(file_path)`: Reads the HTML file
- `html_table_to_dataframe(table, type_value)`: Converts an HTML table to a pandas DataFrame
- `extract_tables_to_excel(html_content, output_file, type_value)`: Extracts all tables and saves them to an Excel file
- `main()`: Handles command-line arguments and orchestrates the extraction process

## Notes
- The script assumes relative URLs in the HTML and prepends "https://scan.merlinchain.io" to all URLs
- Empty URL columns are automatically removed from the output