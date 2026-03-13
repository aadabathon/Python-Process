import re
import sqlite3
from sec_edgar_downloader import Downloader
from bs4 import BeautifulSoup
import pandas as pd

# File path to the 10-K document
SMCI = "C:\\Users\\adams\\Python Projects\\sec-edgar-filings\\SMCI\\10-K\\0001193125-07-190775\\full-submission.txt"
email = "adamsheb414@gmail.com"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Open the 10-K file
with open(SMCI, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, 'html.parser')

# Get the full text of the 10-K document
text = soup.get_text()

# Extracting the "Item 1: Business" section using regex
item_1 = re.search(r'Item\s1\.\s+Business(.*?)Item\s1A\.', text, re.DOTALL | re.IGNORECASE)

if item_1:
    item_1_text = item_1.group(1).strip()
    print("Item 1 Text:")
    print(item_1_text)

# Extracting tables using BeautifulSoup (This part assumes tables are present)
tables = soup.find_all('table')

# Function to clean and convert table data to pandas DataFrame
def extract_table_data(table):
    rows = table.find_all('tr')
    table_data = []
    for row in rows:
        cols = row.find_all(['td', 'th'])  # Extracting both data and header cells
        cols = [ele.text.strip() for ele in cols]
        table_data.append(cols)
    
    return table_data

# Extracting all tables and storing them in pandas DataFrames
financial_data = []
for i, table in enumerate(tables):
    table_data = extract_table_data(table)
    if table_data:
        df = pd.DataFrame(table_data[1:], columns=table_data[0])  # The first row is the header
        financial_data.append(df)

# Now, to identify and extract balance sheet, income statement, and cash flow:
# This part assumes that the relevant tables are already identified as balance sheet, income statement, and cash flow statement

# Save the financial data to an Excel file
with pd. ExcelWriter('financial_statements.xlsx') as writer:
    for i, df in enumerate(financial_data):
        df.to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)

print("Financial data has been saved to 'financial_statements.xlsx'")
